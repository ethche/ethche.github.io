"""Build the static site. Install requirements.txt first; no server runtime needed."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
from string import Template
import markdown

ROOT = Path(__file__).resolve().parent
LAYOUT = Template((ROOT / 'content/layout.html').read_text())


def page(path, title, content, description='Research and writing by Ethan Che.', blog=False):
    return LAYOUT.substitute(title=escape(title), description=escape(description),
                             path=path, content=content,
                             home_current='aria-current="page"' if path == '/' else '',
                             blog_current='aria-current="page"' if blog else '')


def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def read_posts():
    posts = []
    for source in sorted((ROOT / 'content/posts').glob('*.md')):
        parser = markdown.Markdown(extensions=['meta', 'fenced_code', 'tables', 'footnotes'])
        body = parser.convert(source.read_text())
        meta = {key: ' '.join(value) for key, value in parser.Meta.items()}
        if meta.get('draft', 'false').lower() == 'true':
            continue
        published = date.fromisoformat(meta['date'])
        if published > date.today():
            continue
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', source.stem):
            raise ValueError(f'Use a lowercase, hyphenated filename: {source.name}')
        posts.append(dict(title=meta['title'], date=published, body=body,
                          summary=meta.get('summary', ''), path=f'/blog/{source.stem}/'))
    return sorted(posts, key=lambda post: (post['date'], post['path']), reverse=True)


def post_list(posts):
    if not posts:
        return '<p class="meta">No posts yet.</p>'
    rows = ''.join(f'<li><time datetime="{p["date"]}">{p["date"]:%d %b %Y}</time>'
                   f'<a href="{p["path"]}">{escape(p["title"])}</a></li>' for p in posts)
    return f'<ul class="post-list">{rows}</ul>'


def build():
    posts = read_posts()  # Validate all post metadata before replacing generated files.
    papers = json.loads((ROOT / 'content/papers.json').read_text())
    rows = []
    for paper in papers:
        links = paper['links']
        title = escape(paper['title'])
        if links:
            title = f'<a href="{escape(links[0]["url"])}">{title}</a>'
        notes = ' · '.join(paper['notes'])
        resources = ''.join(f'<a href="{escape(link["url"])}">{escape(link["label"])}</a>' for link in links)
        rows.append(f'<li class="paper"><h3>{title}</h3><p>{escape(paper["authors"])}</p>'
                    f'<p class="meta">{escape(notes)}</p><div class="resources">{resources}</div></li>')
    home = Template((ROOT / 'content/home.html').read_text()).substitute(
        papers='<ul class="paper-list">' + '\n'.join(rows) + '</ul>', posts=post_list(posts[:3]))
    write('index.html', page('/', 'Ethan Che', home))
    # This directory contains only generated output, never author-written content.
    if (ROOT / 'blog').exists():
        shutil.rmtree(ROOT / 'blog')
    write('blog/index.html', page('/blog/', 'Blog — Ethan Che',
          '<h1>Blog</h1><p class="meta">Notes on research, learning, and computation.</p>' + post_list(posts), blog=True))
    for post in posts:
        header = (f'<header class="article-header"><h1>{escape(post["title"])}</h1>'
                  f'<time datetime="{post["date"]}">{post["date"]:%d %B %Y}</time></header>')
        write(post['path'].strip('/') + '/index.html', page(post['path'], post['title'] + ' — Ethan Che',
              '<article class="article">' + header + post['body'] + '</article><section><a href="/blog/">← All posts</a></section>',
              description=post['summary'], blog=True))
    write('404.html', page('/404.html', 'Page not found — Ethan Che',
          '<h1>Page not found.</h1><p>This page may have moved. <a href="/">Return home →</a></p>'))
    print(f'Built homepage, {len(posts)} posts, blog index, and 404 page.')


if __name__ == '__main__':
    build()
