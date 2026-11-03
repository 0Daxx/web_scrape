"""
roadmap.sh scraper  —  roadmaps -> projects -> project details (markdown)
=========================================================================
Built with:
  - uv          (venv / dependency management)
  - scrapling   (HTTP fetching + HTML parsing, markdown conversion)

Data sources discovered during probing:
  roadmap.sh is a React-Router v7 SSR app. Every page embeds its loader data
  as a "single fetch" turbo-stream payload inside
  `window.__reactRouterContext.streamController.enqueue("...")` script tags.
  That payload contains the COMPLETE dataset (all roadmaps, all projects per
  roadmap incl. client-side-rendered tabs, and full project content as a
  ProseMirror-style JSON doc).

Strategy (hybrid, verified in test phase):
  * Listing pages (roadmaps / projects): parse embedded stream JSON when
    available (most complete); fall back to plain HTML/CSS extraction.
  * Project detail: render the content doc to clean Markdown; also provide
    the raw markdown extracted from the visible DOM as fallback.

Usage:
  python scraper.py                      # full run (all roadmaps & projects)
  python scraper.py --test               # 1 roadmap (frontend), 2 project details
  python scraper.py --limit-roadmaps 3   # first 3 roadmaps only
  python scraper.py --details            # also scrape every project's detail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------------- 
# Imports with friendly errors
# ----------------------------------------------------------------------------- 
try:
    from scrapling.fetchers import Fetcher
    from scrapling.parser import Selector
except ImportError as exc:  # pragma: no cover
    sys.exit(
        "scrapling is not installed.\n"
        "Create the env with:\n"
        "  uv venv && uv pip install 'scrapling[fetchers]' markdownify\n"
        f"(original error: {exc})"
    )

try:
    from markdownify import markdownify as html_to_markdown
except ImportError:  # pragma: no cover
    sys.exit("markdownify is not installed. Run: uv pip install markdownify")

BASE_URL = "https://roadmap.sh"
OUT_DIR = Path(__file__).parent / "output"

# -----------------------------------------------------------------------------
# Retry helper
# -----------------------------------------------------------------------------


def fetch_with_retries(url: str, *, tries: int = 3, delay: float = 2.0,
                       status_selector: bool = True) -> "Response":
    """GET *url* via scrapling's HTTP Fetcher with basic retry/backoff."""
    last_err: Exception | None = None
    for attempt in range(1, tries + 1):
        try:
            resp = Fetcher.get(url, follow_redirects=True, timeout=60)
            code = getattr(resp, "status", None) or getattr(resp, "status_code", 200)
            if code == 429 or code >= 500:
                raise RuntimeError(f"HTTP {code} for {url}")
            if 400 <= code < 500:
                raise NotFoundError(f"HTTP {code} for {url}")
            return resp
        except NotFoundError:
            raise
        except Exception as err:  # network, timeout, HTTP 429/5xx
            last_err = err
            if attempt < tries:
                wait = delay * attempt
                print(f"    [warn] attempt {attempt}/{tries} failed for {url}: "
                      f"{err} -> retrying in {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
    raise ScrapeError(f"Failed after {tries} attempts: {url} ({last_err})")


class ScrapeError(Exception):
    pass


class NotFoundError(ScrapeError):
    pass


# -----------------------------------------------------------------------------
# React Router "turbo-stream" decoder (minimal, sufficient for roadmap.sh)
# -----------------------------------------------------------------------------
_ENQUEUE_RE = re.compile(r'streamController\.enqueue\(\s*("(?:[^"\\]|\\.)*")\s*\)')
_KEYREF_RE = re.compile(r"^_(\d+)$")


def _decode_key(v: Any) -> str | None:
    """Return the field name a `_N` key refers to, else None."""
    m = _KEYREF_RE.match(str(v))
    if not m:
        return None
    idx = int(m.group(1))
    # reserved negative refs (-5 = undefined etc.) are never names
    if idx < 0:
        return None
    return f"_{idx}"


def _name_from_key(data: list[Any], v: Any) -> str | None:
    m = _KEYREF_RE.match(str(v))
    if not m:
        return None
    idx = int(m.group(1))
    if 0 <= idx < len(data) and isinstance(data[idx], str):
        return data[idx]
    return None


def decode_turbo_stream(html: str) -> list[Any] | None:
    """Return the flat value array of the embedded RR7 single-fetch payload."""
    literals = _ENQUEUE_RE.findall(html)
    if not literals:
        return None
    try:
        chunks = [json.loads(lit) for lit in literals]
        return json.loads("".join(chunks))
    except (json.JSONDecodeError, TypeError):
        return None


def resolve_ref(data: list[Any], ref: Any) -> Any:
    """Resolve an integer index reference into the flat value array.

    Negative refs are turbo-stream sentinels (undefined/null markers) -> None.
    """
    if isinstance(ref, int) and not isinstance(ref, bool):
        if 0 <= ref < len(data):
            return data[ref]
        if ref < 0:
            return None
    return ref


def named_fields(data: list[Any], obj: dict) -> dict:
    """Translate `{_N: value}` keys into their real field names."""
    out: dict[str, Any] = {}
    for k, v in obj.items():
        name = _name_from_key(data, k)
        out[name if name is not None else str(k)] = v
    return out


def _is_key_dict(obj: Any) -> bool:
    return (isinstance(obj, dict) and bool(obj)
            and all(_KEYREF_RE.match(str(k)) for k in obj))


def hydrate(data: list[Any], node: Any, _depth: int = 0, _seen: set | None = None) -> Any:
    """Recursively expand `{_N: idx}` dicts and index references into real objects."""
    if _depth > 400:
        return None
    if _seen is None:
        _seen = set()
    nid = id(node)
    if isinstance(node, (dict, list)):
        if nid in _seen:
            return "<cycle>"
        _seen = _seen | {nid}

    if isinstance(node, list):
        return [hydrate(data, v, _depth + 1, _seen) for v in node]
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for k, v in node.items():
            key = k
            m = _KEYREF_RE.match(str(k))
            if m:
                name = data[int(m.group(1))] if int(m.group(1)) < len(data) else None
                if isinstance(name, str):
                    key = name
            out[key] = hydrate(data, v, _depth + 1, _seen)
        return out
    return node


def load_page_graph(url: str) -> tuple[list[Any] | None, Selector]:
    """Fetch a page; return (hydrated-flat-array-or-None, DOM selector)."""
    resp = fetch_with_retries(url)
    body = getattr(resp, "body", None)
    if isinstance(body, bytes):
        body = body.decode("utf-8", "replace")
    if not isinstance(body, str):
        body = str(resp.html if hasattr(resp, "html") else resp)
    html = body
    data = decode_turbo_stream(html)
    dom = Selector(html)
    return data, dom


# -----------------------------------------------------------------------------
# ProseMirror-style content doc -> Markdown
# -----------------------------------------------------------------------------

def content_doc_to_markdown(doc: Any) -> str:
    """Convert roadmap.sh's rich-text content JSON into Markdown."""
    if not isinstance(doc, dict):
        return ""

    def inline(node: dict) -> str:
        text = node.get("text", "")
        for mark in node.get("marks") or []:
            t = (mark.get("type") or "").lower()
            attrs = mark.get("attrs") or {}
            if t == "bold":
                text = f"**{text}**"
            elif t == "italic":
                text = f"*{text}*"
            elif t == "code":
                text = f"`{text}`"
            elif t == "link":
                href = attrs.get("href", "")
                text = f"[{text}]({href})" if href else text
        return text

    def block(node: dict, level_stack: list[str]) -> str:
        ntype = node.get("type")
        children = node.get("content") or []
        if ntype == "paragraph":
            return "".join(inline(c) if c.get("type") == "text" else block(c, level_stack)
                           for c in children) + "\n\n"
        if ntype == "heading":
            lvl = int((node.get("attrs") or {}).get("level", 2))
            txt = "".join(inline(c) if c.get("type") == "text" else block(c, level_stack)
                          .strip() for c in children)
            return f"{'#' * min(lvl + 1, 6)} {txt}\n\n"
        if ntype == "bulletList":
            rows = []
            for li in children:
                inner = " ".join(
                    (block(c, level_stack).strip()) for c in (li.get("content") or [])
                )
                rows.append(f"* {inner}")
            return "\n".join(rows) + "\n\n"
        if ntype == "orderedList":
            rows = []
            for i, li in enumerate(children, 1):
                inner = " ".join(
                    (block(c, level_stack).strip()) for c in (li.get("content") or [])
                )
                rows.append(f"{i}. {inner}")
            return "\n".join(rows) + "\n\n"
        if ntype == "listItem":
            return "".join(block(c, level_stack) for c in children)
        if ntype == "codeBlock":
            attrs = node.get("attrs") or {}
            lang = attrs.get("language") or ""
            code = "".join(c.get("text", "") for c in children)
            return f"```{lang}\n{code.rstrip()}\n```\n\n"
        if ntype == "horizontalRule":
            return "---\n\n"
        if ntype == "image":
            attrs = node.get("attrs") or {}
            src = attrs.get("src", "")
            alt = attrs.get("alt", "") or ""
            return f"![{alt}]({src})\n\n"
        # generic fallback: recurse
        return "".join(block(c, level_stack) for c in children)

    parts = [block(n, []) for n in (doc.get("content") or [])]
    md = "".join(parts)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


# -----------------------------------------------------------------------------
# Scrapers
# -----------------------------------------------------------------------------

@dataclass
class Roadmap:
    slug: str
    title: str
    category: str = ""
    url: str = ""


def scrape_roadmaps() -> list[Roadmap]:
    """All roadmaps from https://roadmap.sh/roadmaps (stream JSON, HTML fallback)."""
    url = f"{BASE_URL}/roadmaps"
    print(f"[1/3] Fetching roadmaps list: {url}")
    data, dom = load_page_graph(url)
    roadmaps: list[Roadmap] = []
    skip_slugs = {"roadmaps", "guides", "about", "best-practices"}

    if data is not None:
        # Find objects that look like roadmaps: have slug + title (+ category)
        hydrated_roots = []
        # top-level structure: data[0] is {_1: loaderData,...}; walk everything
        seen_ids: set[int] = set()

        def walk(node: Any, depth: int = 0) -> Any:
            if depth > 250 or id(node) in seen_ids:
                return None
            if isinstance(node, dict):
                seen_ids.add(id(node))
                resolved = {}
                for k, v in node.items():
                    m = _KEYREF_RE.match(str(k))
                    key = k
                    if m and int(m.group(1)) < len(data) and isinstance(data[int(m.group(1))], str):
                        key = data[int(m.group(1))]
                    resolved[key] = resolve_ref(data, v)
                return resolved
            return None

        # brute-force scan: any dict object whose values include a known-looking slug
        slugs_seen: set[str] = set()
        for obj in data:
            if not isinstance(obj, dict):
                continue
            r = walk(obj)
            if not isinstance(r, dict):
                continue
            slug = r.get("slug")
            title = r.get("title")
            if (isinstance(slug, str) and isinstance(title, str)
                    and re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug)
                    and slug not in slugs_seen and slug not in skip_slugs
                    and ("category" in r or "isPrintableRoadmap" in r or "order" in r)):
                slugs_seen.add(slug)
                roadmaps.append(Roadmap(slug=slug, title=title,
                                        category=str(r.get("category", "")),
                                        url=f"{BASE_URL}/{slug}"))

    if not roadmaps:  # HTML fallback
        print("    [info] stream payload unusable -> falling back to HTML anchors")
        blocked = {"signup", "login", "ai", "packs", "newsletters", "roadmaps",
                   "guides", "about", "terms", "privacy", "projects", "skill-combos",
                   "skill-combo", "best-practices", "cdn-cgi"}
        for a in dom.css("a"):
            href = (a.attrib.get("href") or "").strip("/")
            text = (a.text or "").strip()
            if (href and text and "/" not in href and href not in blocked
                    and href not in {r.slug for r in roadmaps}):
                roadmaps.append(Roadmap(slug=href, title=text, url=f"{BASE_URL}/{href}"))

    print(f"    -> found {len(roadmaps)} roadmaps")
    return roadmaps


def scrape_roadmap_projects(slug: str) -> tuple[list[dict], str]:
    """Projects for one roadmap: https://roadmap.sh/<slug>/projects

    Returns (projects, source) where source is 'stream' or 'html'.
    Each project dict: slug/title/description/level/tags/related_topics/url.
    """
    url = f"{BASE_URL}/{slug}/projects"
    print(f"      - projects: {url}")
    data, dom = load_page_graph(url)
    projects: list[dict] = []
    source = "stream"

    if data is not None:
        # Project records are dicts whose translated keys contain
        # {'slug','title','description','difficulty'}
        def ref_names(ref_list) -> list[str]:
            out: list[str] = []
            if isinstance(ref_list, list):
                for it in ref_list:
                    item = resolve_ref(data, it)
                    if isinstance(item, str):
                        out.append(item)
                    elif isinstance(item, dict):
                        nf = named_fields(data, item)
                        nm = resolve_ref(data, nf.get("name"))
                        if isinstance(nm, str):
                            out.append(nm)
            return out

        for obj in data:
            if not isinstance(obj, dict):
                continue
            f = named_fields(data, obj)
            if {"slug", "title", "description", "difficulty"} <= set(f):
                pslug = resolve_ref(data, f["slug"])
                if not isinstance(pslug, str):
                    continue
                projects.append({
                    "slug": pslug,
                    "title": resolve_ref(data, f.get("title")) or pslug,
                    "description": resolve_ref(data, f.get("description")) or "",
                    "level": resolve_ref(data, f.get("difficulty")),
                    "type": resolve_ref(data, f.get("type")),
                    "tags": ref_names(resolve_ref(data, f.get("topics"))),
                    "related_topics": ref_names(resolve_ref(data, f.get("skills"))),
                    "url": f"{BASE_URL}/projects/{pslug}",
                })

    if not projects:  # HTML fallback (server-rendered cards only)
        source = "html"
        print(f"        [info] using HTML anchor fallback for {slug}")
        for a in dom.css('a[href^="/projects/"]'):
            href = a.attrib.get("href", "")
            pslug = href.rsplit("/", 1)[-1]
            if not pslug or pslug in {p["slug"] for p in projects}:
                continue
            card_title = (a.text or "").strip()
            projects.append({
                "slug": pslug,
                "title": card_title or pslug.replace("-", " ").title(),
                "description": "",
                "level": None,
                "tags": [],
                "related_topics": [],
                "url": f"{BASE_URL}{href}",
            })

    # de-dupe by slug, keep order
    uniq, seen = [], set()
    for p in projects:
        if p["slug"] not in seen:
            seen.add(p["slug"])
            uniq.append(p)
    print(f"        -> {len(uniq)} projects ({source})")
    return uniq, source


def scrape_project_detail(project_slug: str) -> dict:
    """Full project detail at https://roadmap.sh/projects/<slug>.

    Extracts metadata from the embedded loader JSON and renders the complete
    description/content to Markdown. Falls back to DOM->markdown conversion.
    """
    url = f"{BASE_URL}/projects/{project_slug}"
    print(f"      - detail: {url}")
    detail: dict[str, Any] = {"slug": project_slug, "url": url}
    data, dom = load_page_graph(url)

    content_md = ""
    if data is not None:
        # locate the project record: dict with 'slug'==project_slug and 'content'
        def named(obj: dict) -> dict:
            out = {}
            for k, v in obj.items():
                kk = k
                m = _KEYREF_RE.match(str(k))
                if m and int(m.group(1)) < len(data) and isinstance(data[int(m.group(1))], str):
                    kk = data[int(m.group(1))]
                out[kk] = v
            return out

        for obj in data:
            if not isinstance(obj, dict):
                continue
            f = named(obj)
            sv = resolve_ref(data, f.get("slug"))
            if sv == project_slug and "content" in f:
                content_ref = resolve_ref(data, f["content"])
                content_doc = hydrate(data, content_ref) if content_ref is not None else None
                detail.update({
                    "title": resolve_ref(data, f.get("title")),
                    "description": resolve_ref(data, f.get("description")),
                    "level": resolve_ref(data, f.get("level")),
                    "roadmap_id": resolve_ref(data, f.get("_id") if "_id" in f else None),
                })
                # tags / related are lists of refs -> resolve names
                for fld, key in (("tags", "name"), ("related", "name")):
                    vals = f.get(fld)
                    names = []
                    if isinstance(vals, list):
                        for it in vals:
                            item = resolve_ref(data, it)
                            if isinstance(item, dict):
                                nf = named(item)
                                nm = resolve_ref(data, nf.get(key))
                                if isinstance(nm, str):
                                    names.append(nm)
                            elif isinstance(item, str):
                                names.append(item)
                    detail[fld] = names
                if isinstance(content_doc, dict):
                    content_md = content_doc_to_markdown(content_doc)
                break

    # fallbacks
    if not detail.get("title"):
        h1 = dom.css("h1::text")
        detail["title"] = (h1[0].strip() if h1 else project_slug)
    if not content_md:
        pc = dom.css("div.page-container")
        if pc:
            content_md = html_to_markdown(str(pc[0]), heading_style="ATX").strip() + "\n"
            detail["content_source"] = detail.get("content_source", "dom-markdownify")

    detail.setdefault("content_source", "content-json")
    detail["markdown"] = content_md
    print(f"        -> ok: '{detail.get('title')}' ({len(content_md)} chars markdown)")
    return detail


# -----------------------------------------------------------------------------
# Helpers / orchestration
# -----------------------------------------------------------------------------

def safe_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s or "unnamed"


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="roadmap.sh scraper (scrapling)")
    ap.add_argument("--test", action="store_true",
                    help="Test mode: 1 roadmap (frontend), list projects, 2 details")
    ap.add_argument("--limit-roadmaps", type=int, default=None)
    ap.add_argument("--limit-projects-per-roadmap", type=int, default=None)
    ap.add_argument("--no-details", action="store_true",
                    help="Skip project-detail scraping (listing only)")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    started = time.time()

    try:
        roadmaps = scrape_roadmaps()
        if not roadmaps:
            print("[error] no roadmaps extracted", file=sys.stderr)
            return 1
        save_json(OUT_DIR / "roadmaps.json", [r.__dict__ for r in roadmaps])

        if args.test:
            roadmaps = [r for r in roadmaps if r.slug == "frontend"] or roadmaps[:1]

        if args.limit_roadmaps:
            roadmaps = roadmaps[: args.limit_roadmaps]

        catalog: list[dict] = []
        errors: list[dict] = []
        for r in roadmaps:
            entry = {"roadmap": r.__dict__, "source": None, "projects": []}
            try:
                projects, source = scrape_roadmap_projects(r.slug)
                entry["source"] = source
                entry["projects"] = projects

                if args.test:
                    projects = projects[:2]
                if args.limit_projects_per_roadmap:
                    projects = projects[: args.limit_projects_per_roadmap]

                if not args.no_details:
                    for p in projects:
                        try:
                            d = scrape_project_detail(p["slug"])
                            md_path = (OUT_DIR / "projects" / f"{safe_name(d['slug'])}.md")
                            md_path.parent.mkdir(parents=True, exist_ok=True)
                            front = (f"# {d.get('title')}\n\n"
                                     f"> {d.get('description','')}\n\n"
                                     f"- Level: {d.get('level')}\n"
                                     f"- Tags: {', '.join(d.get('tags') or [])}\n"
                                     f"- URL: {d.get('url')}\n\n---\n\n")
                            md_path.write_text(front + d.get("markdown", ""),
                                               encoding="utf-8")
                            entry.setdefault("details", []).append(
                                {k: v for k, v in d.items() if k != "markdown"})
                        except ScrapeError as e:
                            errors.append({"stage": "detail", "project": p["slug"],
                                           "error": str(e)})
                            print(f"        [error] detail {p['slug']}: {e}",
                                  file=sys.stderr)
                        time.sleep(0.3)  # be polite
            except ScrapeError as e:
                errors.append({"stage": "projects", "roadmap": r.slug, "error": str(e)})
                print(f"    [error] projects {r.slug}: {e}", file=sys.stderr)
            catalog.append(entry)
            save_json(OUT_DIR / "catalog.json", catalog)  # incremental checkpoint
            if args.test:
                break
            time.sleep(0.3)

        save_json(OUT_DIR / "errors.json", errors)
        n_proj = sum(len(e["projects"]) for e in catalog)
        print(f"\nDone in {time.time()-started:.1f}s | "
              f"roadmaps={len(catalog)} projects={n_proj} errors={len(errors)}")
        print(f"Outputs in {OUT_DIR}/ : roadmaps.json, catalog.json, "
              f"errors.json, projects/*.md")
        return 0
    except KeyboardInterrupt:
        print("\n[interrupted] partial results saved to output/", file=sys.stderr)
        return 130
    except Exception as e:  # last-resort guard
        print(f"[fatal] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
