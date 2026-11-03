Photo Showcase
beginner

Photo Showcase
==============

Build an HTML photo showcase page with proper alt text, figures with captions, and an embedded video.

Start building, submit solution and get feedback from the community.

Start Working
The goal of this project is to teach you how to handle images, captions, and embedded media in HTML. You will build a page that displays a small collection of images with proper alt text, captions, and one embedded video. Do not style the page; styling will be addressed in a later project. Focus here on the markup that decides how the media is loaded, described, and announced.

In this project, you are required to build a single HTML page that showcases a small collection of photos or images.

You can use your own images, public images, or placeholder URLs - the focus is on the markup, not the photos.

Key requirements:

* **A semantic page**: Use `<header>`, `<main>`, and `<footer>` to structure the page itself.
* **At least six images** inside the main content. Each `<img>` must include:

  + A `src` that points to a real image (a local file or a public URL).
  + A useful `alt` attribute that describes the image, not the filename.
  + `width` and `height` attributes to reserve layout space and prevent the page from jumping as images load.
* **Captions on at least three images** using `<figure>` and `<figcaption>`. Remember: the `alt` text stands in for the image when it cannot be seen; the caption gives extra context to everyone.
* **One decorative image** (put any image) with `alt=""` so screen readers skip it. Leaving the attribute off entirely is different - always include it.
* **One embedded** **`<video>`** with `controls`, a `poster` image, and fallback text between the opening and closing tags. If you do not have a video file, use any small `.mp4` you have on your computer; the player UI will still appear from the markup alone.
* **Head metadata**: Set `<title>`, `<meta charset>`, and `<meta viewport>`.

### Submission Checklist:

* A single HTML page with header, main, and footer regions.
* At least six `<img>` elements, each with `src`, `alt`, `width`, and `height`.
* Three or more images wrapped in `<figure>` with `<figcaption>`.
* One decorative image with `alt=""`.
* One `<video>` with `controls`, `poster`, and fallback content.
* Head metadata set correctly.

By completing this project, you will leave with a clear sense of how `alt` text is different from a caption, why dimensions on `<img>` matter for layout, and how `<video>` builds its player from the attributes you write. These habits pay off everywhere images and media appear later.

