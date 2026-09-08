# HAYTERWAVE — REQUIEM · screening

The screening page for **HAYTERWAVE — REQUIEM (QUAM OLIM)**: Mozart's Requiem
reimagined as tech house at 128 BPM, a gothic cathedral built around the music.

Live at https://hayterfinance-bit.github.io/requiem/ — unlisted (noindex, robots
disallow), free GitHub Pages, no build step. Everything is in `index.html` and
`assets/`.

## Going live with the film — the one step

Edit `assets/film.json` and point it at the release assets:

```json
{
  "mp4": "https://github.com/hayterfinance-bit/requiem/releases/download/v1/REQUIEM_QUAM_OLIM_1080p.mp4",
  "mov": "https://github.com/hayterfinance-bit/requiem/releases/download/v1/REQUIEM_QUAM_OLIM_1080p_PCM24.mov",
  "status": "live"
}
```

Commit and push. The page reads that file on load: with `mp4` set the player
plays; with `mov` set the "Download lossless" button appears. Leave a key
`null` to keep it hidden.

## Attaching the film as a release asset

```
gh release create v1 --repo hayterfinance-bit/requiem --title "REQUIEM · QUAM OLIM" --notes "1080p screening master" REQUIEM_QUAM_OLIM_1080p.mp4 REQUIEM_QUAM_OLIM_1080p_PCM24.mov
```

Limits: a single release asset may be up to 2 GB; there is no total cap on
releases. Files in the repository itself should stay under 100 MB, so the film
goes on the release, never in the tree. The page's own assets (`og.jpg`,
`poster.jpg`) are small on purpose.

The browser file should be H.264 with FLAC audio in MP4 (Chrome, Firefox and
Safari play it); the download should be H.264 with 24-bit PCM in MOV.

## Social card

`assets/og.jpg` is 1200 × 630 and is referenced with absolute URLs in the
Open Graph and Twitter meta tags. Chat apps cache the card the first time a
link is pasted, so change the image file name if the card ever needs to
change.
