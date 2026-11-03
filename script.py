import json
import time
import logging
from scrapling import Fetcher
from urllib.parse import urljoin

# --- Configuration & Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://roadmap.sh"
OUTPUT_FILE = "roadmap_sh_data.json"

# Initialize Scrapling Fetcher
# auto_match=True helps automatically handle some anti-bot protections and parsing optimizations
fetcher = Fetcher(auto_match=True)

def get_safe_text(element):
    """Helper to safely extract text from a scrapling element."""
    if element:
        # Clean up whitespace
        return ' '.join(element.text.strip().split())
    return ""

def scrape_roadmaps_list():
    """Scrapes the main roadmaps index page to get all roadmap URLs and basic info."""
    logger.info("Fetching roadmaps list...")
    page = fetcher.get(f"{BASE_URL}")
    roadmaps = []
    
    # roadmap.sh uses a grid of cards. We look for links that point to specific roadmaps.
    # We filter out links that go to /projects, /best-practices, etc.
    cards = page.css('a.group[href^="/"]') 
    
    for card in cards:
        href = card.attrib.get('href', '')
        
        # Filter to only get main roadmaps (e.g., /frontend, /backend)
        if href.startswith('/projects') or href.count('/') > 1 or href == '/':
            continue
            
        title_elem = card.css('h3, h2, span.font-bold')
        desc_elem = card.css('p, span.text-sm')
        
        roadmaps.append({
            "title": get_safe_text(title_elem),
            "url": urljoin(BASE_URL, href),
            "description": get_safe_text(desc_elem),
            "type": "roadmap"
        })
        
    logger.info(f"Found {len(roadmaps)} roadmaps.")
    return roadmaps

def scrape_projects_list():
    """Scrapes the main projects index page to get all project URLs and basic info."""
    logger.info("Fetching projects list...")
    page = fetcher.get(f"{BASE_URL}/projects")
    projects = []
    
    # Projects are also in a grid of cards
    cards = page.css('a.group[href^="/projects/"]')
    
    for card in cards:
        href = card.attrib.get('href', '')
        if not href.startswith('/projects/') or href == '/projects':
            continue
            
        title_elem = card.css('h3, h2, span.font-bold')
        desc_elem = card.css('p, span.text-sm')
        # Difficulty is often in a specific badge or span
        diff_elem = card.css('span[class*="difficulty"], span.badge') 
        
        projects.append({
            "title": get_safe_text(title_elem),
            "url": urljoin(BASE_URL, href),
            "description": get_safe_text(desc_elem),
            "difficulty": get_safe_text(diff_elem),
            "type": "project"
        })
        
    logger.info(f"Found {len(projects)} projects.")
    return projects

def scrape_detail_page(url, item_type):
    """Scrapes the detailed textual content from a specific roadmap or project page."""
    logger.info(f"Scraping details for: {url}")
    try:
        page = fetcher.get(url)
        
        # Extract main textual content. 
        # We target the main article/content area to avoid scraping headers/footers.
        main_content = page.css('main, article, div[class*="content"]')
        
        sections = []
        if main_content:
            # Extract headings and their following paragraphs to create structured sections
            headings = main_content.css('h1, h2, h3, h4')
            for heading in headings:
                heading_text = get_safe_text(heading)
                if not heading_text:
                    continue
                
                # Get text of all paragraphs following this heading until the next heading
                # (Simplified approach: just grab all text in the main content for NLP chunking)
                
        # For NLP purposes, getting the raw, clean text of the page is often best for chunking
        full_text = get_safe_text(main_content)
        
        return {
            "full_text_content": full_text,
            "headings": [get_safe_text(h) for h in page.css('h1, h2, h3') if get_safe_text(h)],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return {"status": "failed", "error": str(e)}

def main():
    start_time = time.time()
    
    # 1. Get Lists
    roadmaps = scrape_roadmaps_list()
    projects = scrape_projects_list()
    
    # 2. Scrape Details for Roadmaps
    logger.info("Starting detailed scraping for roadmaps...")
    for i, roadmap in enumerate(roadmaps):
        details = scrape_detail_page(roadmap['url'], 'roadmap')
        roadmap['details'] = details
        # Be polite to the server
        time.sleep(1.5) 
        
    # 3. Scrape Details for Projects
    logger.info("Starting detailed scraping for projects...")
    for i, project in enumerate(projects):
        details = scrape_detail_page(project['url'], 'project')
        project['details'] = details
        time.sleep(1.5)
        
    # 4. Save to File
    final_data = {
        "metadata": {
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_roadmaps": len(roadmaps),
            "total_projects": len(projects)
        },
        "roadmaps": roadmaps,
        "projects": projects
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
        
    logger.info(f"Successfully saved data to {OUTPUT_FILE}")
    logger.info(f"Total time taken: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()