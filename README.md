# Idlewild Heritage Trail — website

This is the site that each sign's QR code will point to: one page per stop,
with a photo, an audio player for the recorded story, and a transcript.

## How this is organized

- `data/stops.json` — the actual content. One entry per stop: name,
  description (used as the on-page transcript), and `audio_url` (empty
  until that stop's recording is hosted somewhere).
- `templates/` — the two HTML templates (one stop page, one index/directory
  page). Edit these if you want to change the *layout*; edit `stops.json`
  if you want to change the *content*.
- `assets/css/style.css` — all the styling, pulled from the printed sign's
  look (dark brown/orange, the headline typeface, etc).
- `assets/img/stops/` — put a stop's photo here, named to match its slug
  (see below). Empty for now — pages show a "Photo coming soon" box until
  a file shows up here.
- `assets/audio/` — optional local home for audio files if you decide to
  host them in this same repo (see HOSTING-AUDIO.md for the tradeoffs).
- `build.py` — regenerates the whole site from the data + templates into
  `docs/`. Run this after any edit.
- `docs/` — the generated, ready-to-publish site. This is what GitHub
  Pages actually serves. Don't hand-edit anything in here — it gets wiped
  and rebuilt every time you run `build.py`.
- `CONTENT-CHECKLIST.md` — auto-generated every build. Shows which stops
  still need a photo and/or a recording, straight from the data.

## Making a change

1. Edit `data/stops.json` (fix a typo, add an `audio_url`, etc.), or drop
   a photo into `assets/img/stops/<slug>.jpg`.
2. Run:
   ```
   python3 build.py
   ```
3. Open `docs/index.html` in a browser to check it, or push to GitHub
   (see below) and refresh the live site.

### Naming photos correctly

Each stop has a `slug` in `stops.json`, e.g. Morton's Motel is
`mortons-motel`. Save its photo as:

```
assets/img/stops/mortons-motel.jpg
```

(`.jpeg` and `.png` also work.) Run `python3 build.py` again and it picks
the photo up automatically — no HTML to touch.

## Publishing to GitHub Pages (you said you already have a GitHub account)

1. Create a new repository on GitHub (public repos get free Pages
   hosting — call it something like `idlewild-heritage-trail`).
2. From inside this folder:
   ```
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub: go to the repo's **Settings → Pages**. Under "Build and
   deployment," set **Source** to "Deploy from a branch," branch **main**,
   folder **/docs**. Save.
4. GitHub will give you a URL like
   `https://<your-username>.github.io/<repo-name>/` — that's your live
   site. It can take a minute or two to go live the first time.
5. (Optional) If you buy a custom domain later, GitHub Pages supports
   pointing it at this same repo — you'd just add a `CNAME` file and
   update your domain's DNS. Ask me when you're ready and I'll walk you
   through it.

Each stop's live page will be at:

```
https://<your-username>.github.io/<repo-name>/stops/<slug>.html
```

Those exact URLs are what you'll turn into QR codes for the velcro tags —
so it's worth finalizing the GitHub repo name before generating the final
batch of QR codes (renaming the repo later would change every URL).

## Still needed from you

- The real Idlewild Heritage Trail logo file (I used a placeholder "IH"
  circle badge).
- Any official brand colors / exact hex codes, if they differ from what I
  sampled off the sign photo.
- Photos for each stop (see naming convention above) — `CONTENT-CHECKLIST.md`
  tracks what's missing.
- Audio recordings, once produced — see `HOSTING-AUDIO.md` for where to
  put them.
