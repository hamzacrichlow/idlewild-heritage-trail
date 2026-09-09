#!/usr/bin/env python3
"""
Idlewild Heritage Trail — static site builder.

Reads data/stops.json, fills in templates/*.html, and writes the finished
site into docs/ (GitHub Pages can serve straight from a repo's /docs
folder on the main branch — no extra branch or Actions workflow needed).

Run it again any time you:
  - edit a stop's text in data/stops.json
  - drop a real photo into assets/img/stops/<slug>.jpg (.jpg/.jpeg/.png all work)
  - fill in a stop's "audio_url" once that recording is hosted somewhere
    (see HOSTING-AUDIO.md)

Usage:
    python3 build.py
"""
import json
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "stops.json"
TEMPLATES = ROOT / "templates"
ASSETS_SRC = ROOT / "assets"
DOCS = ROOT / "docs"
CNAME_FILE = ROOT / "CNAME"

PHOTO_EXTS = [".jpg", ".jpeg", ".png"]


def find_photos(slug: str):
    """Finds a stop's photo(s). The first is named `<slug>.<ext>`; extra
    photos are `<slug>-2.<ext>`, `<slug>-3.<ext>`, etc. (drop them into
    assets/img/stops/ with those names and re-run the build)."""
    photos = []
    i = 1
    while True:
        name = slug if i == 1 else f"{slug}-{i}"
        found = None
        for ext in PHOTO_EXTS:
            candidate = ASSETS_SRC / "img" / "stops" / f"{name}{ext}"
            if candidate.exists():
                found = f"assets/img/stops/{name}{ext}"
                break
        if not found:
            break
        photos.append(found)
        i += 1
    return photos


def photo_block(stop, from_stop_page=True):
    prefix = "../" if from_stop_page else ""
    photos = find_photos(stop["slug"])
    if not photos:
        return (
            '<div class="stop-photo placeholder"><span>Photo coming soon</span>'
            f'<code>assets/img/stops/{stop["slug"]}.jpg</code></div>'
        )
    if len(photos) == 1:
        return (
            f'<img class="stop-photo" src="{prefix}{photos[0]}" '
            f'alt="{html.escape(stop["name"])}">'
        )
    imgs = "\n".join(
        f'    <img class="stop-photo gallery" src="{prefix}{p}" '
        f'alt="{html.escape(stop["name"])}">'
        for p in photos
    )
    return f'<div class="stop-photos">\n{imgs}\n  </div>'


def audio_block(stop):
    url = stop.get("audio_url", "").strip()
    if not url:
        return '<div class="coming-soon">Recording coming soon.</div>'
    src = html.escape(url)
    return f'''<div class="audio-player">
  <audio class="player-audio" preload="metadata"><source src="{src}"></audio>
  <button type="button" class="player-toggle" aria-label="Play">
    <svg class="icon icon-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
    <svg class="icon icon-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" hidden><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
  </button>
  <span class="player-time player-time-current">0:00</span>
  <input type="range" class="player-seek" value="0" min="0" max="0" step="0.1" aria-label="Seek">
  <span class="player-time player-time-duration">0:00</span>
  <button type="button" class="player-mute" aria-label="Mute">
    <svg class="icon icon-volume" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    <svg class="icon icon-muted" viewBox="0 0 24 24" aria-hidden="true" hidden><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 9l5 5M21 9l-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
  </button>
</div>'''


def next_link_block(next_stop):
    if not next_stop:
        return ""
    return (
        f'<a class="next-link" href="{next_stop["slug"]}.html">'
        f'Go to next stop &rarr;</a>'
    )


def render_stop(stop, total, template, next_stop=None):
    out = template
    out = out.replace("{{NAME}}", html.escape(stop["name"]))
    out = out.replace("{{NUMBER}}", str(stop["number"]))
    out = out.replace("{{TOTAL}}", str(total))
    out = out.replace("{{DESCRIPTION_HTML}}", html.escape(stop["description"]))
    out = out.replace("{{DESCRIPTION_PLAIN}}", html.escape(stop["description"][:160]))
    out = out.replace("{{PHOTO_BLOCK}}", photo_block(stop, from_stop_page=True))
    out = out.replace("{{AUDIO_BLOCK}}", audio_block(stop))
    out = out.replace("{{NEXT_LINK}}", next_link_block(next_stop))
    return out


def render_index(stops, template):
    items = []
    for s in stops:
        items.append(
            f'    <li><a href="stops/{s["slug"]}.html">'
            f'<span class="num">{s["number"]:02d}</span>'
            f'<span class="name">{html.escape(s["name"])}</span>'
            "</a></li>"
        )
    return template.replace("{{STOP_LIST_ITEMS}}", "\n".join(items))


def main():
    stops = json.loads(DATA_FILE.read_text())
    total = len(stops)

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    (DOCS / "stops").mkdir()

    # Copy assets as-is
    shutil.copytree(ASSETS_SRC, DOCS / "assets")

    # Custom domain for GitHub Pages — must be re-copied into docs/ on every
    # build since docs/ gets wiped above (see CNAME file at repo root).
    if CNAME_FILE.exists():
        shutil.copy2(CNAME_FILE, DOCS / "CNAME")

    stop_template = (TEMPLATES / "stop_template.html").read_text()
    index_template = (TEMPLATES / "index_template.html").read_text()

    for i, stop in enumerate(stops):
        next_stop = stops[i + 1] if i + 1 < len(stops) else None
        page = render_stop(stop, total, stop_template, next_stop)
        (DOCS / "stops" / f"{stop['slug']}.html").write_text(page)

    (DOCS / "index.html").write_text(render_index(stops, index_template))

    # Internal production checklist — NOT linked from the public site.
    # Tracks what still needs to be gathered per stop.
    checklist_lines = ["# Content checklist (internal — not part of the public site)\n"]
    for s in stops:
        has_photo = "photo on file" if find_photos(s["slug"]) else "NEEDS PHOTO"
        has_audio = "audio linked" if s.get("audio_url", "").strip() else "NEEDS RECORDING"
        checklist_lines.append(
            f"- [{'x' if find_photos(s['slug']) else ' '}] **{s['number']:02d}. {s['name']}** "
            f"— {has_photo}; {has_audio}. _{s.get('photo_notes','')}_"
        )
    (ROOT / "CONTENT-CHECKLIST.md").write_text("\n".join(checklist_lines) + "\n")

    print(f"Built {total} stop pages + index into {DOCS}")
    print("Wrote CONTENT-CHECKLIST.md with what's still missing per stop.")


if __name__ == "__main__":
    main()
