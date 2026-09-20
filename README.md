# Ethan Che’s website

A small static website with one stylesheet, system fonts, and no browser JavaScript.
Generated HTML is committed, so GitHub Pages can serve the repository root directly.

## Edit and preview

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
python3 -m http.server 8000
```

Open http://localhost:8000. Edit `content/home.html` for the introduction and
sections, `content/papers.json` for research, `content/layout.html` for the shared
layout, and `assets/style.css` for design. Rebuild after content edits.

## Publish a blog post

Copy `content/posts/example.md` to `content/posts/your-post-slug.md`. Set its
Title, Date (YYYY-MM-DD), and Summary, then write Markdown below the blank line.
Set `Draft: false` and run `python build.py` in your virtual environment.
Drafts and future-dated posts are excluded. Published posts appear automatically
on the homepage and blog index.

The filename becomes `/blog/your-post-slug/`; keep it stable after publishing.
Use root-relative image paths such as `/images/figure.png`. Code fences, tables,
and footnotes are supported. Content is trusted author-written Markdown/HTML.
The example stays unpublished; there are no invented posts on the public site.

Commit both source and generated files, then push through your usual GitHub Pages
workflow. This redesign does not change deployment settings.

`build.py` owns `blog/`, `index.html`, and `404.html`; don’t edit those
outputs by hand. PDF and research image URLs are preserved. The old Bootstrap,
jQuery, PHP publication tools, duplicate assets, and template boilerplate have
been removed. The previous site used the [Academic Responsive template](https://github.com/dmsl/academic-responsive-template).
