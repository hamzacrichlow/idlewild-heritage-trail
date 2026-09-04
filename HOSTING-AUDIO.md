# Hosting the 25 audio recordings

Recap of what we landed on, and exactly how to wire a recording into a
page once it's ready.

## Recommended: same repo as the site

Put finished mp3s in `assets/audio/`, named to match the stop's slug, e.g.:

```
assets/audio/mortons-motel.mp3
```

Then in `data/stops.json`, set that stop's `audio_url` to the relative
path GitHub Pages will serve it at:

```json
"audio_url": "../assets/audio/mortons-motel.mp3"
```

Run `python3 build.py` — the page automatically switches from "Recording
coming soon" to a real audio player. No other changes needed.

Keep an eye on total repo size (soft cap ~1GB on GitHub Pages) — 25 voice
recordings as mp3 will be a small fraction of that, so this is fine for
this project's scale.

## Backup copy: Internet Archive

Worth mirroring the same files to archive.org as a free, permanent backup
independent of GitHub — belt and suspenders for something meant to
outlive a single hosting decision. If you ever want to use an Internet
Archive link instead of/alongside the repo copy, just paste that link into
`audio_url` instead.

## Optional nicer player: Spotify for Creators

If you'd rather have a polished embeddable player instead of the plain
browser audio bar, upload the recordings there as "episodes" and swap in
their embed code inside `templates/stop_template.html` (in place of the
`{{AUDIO_BLOCK}}` output) — ask me and I'll wire that variant in.

## Recording tips

- A phone voice memo is plenty of quality for this — just record
  somewhere quiet, away from wind/AC noise.
- Keep each story to roughly 60–120 seconds; people are standing outside
  reading a sign, not sitting down for a podcast.
- Free editing: Audacity, if you want to trim silence or normalize
  volume before uploading.
