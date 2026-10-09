# Balcony Deck Survey

A static site. Deck geometry measured from a Gaussian splat of the balcony:
interactive 3D model rendered as the Gaussian splat itself, dimensioned plan, section, clearance table, and a
photographic horizon placed by the compass headings in the photos' EXIF.

## Publish on GitHub Pages

1. Create a repository on GitHub — public, or private on a plan that allows Pages.
2. Upload **everything in this folder**, keeping the directory structure:

   ```
   index.html
   .nojekyll
   assets/
   data/
   ```

   In the browser: **Add file → Upload files**, then drag the `assets` and
   `data` folders in along with `index.html`. Note that GitHub's web uploader
   silently skips dotfiles, so `.nojekyll` may not make it — see below.

3. **Settings → Pages**. Under *Build and deployment* set **Source: Deploy from
   a branch**, branch `main`, folder `/ (root)`. Save.
4. Wait a minute or two. The URL is `https://<user>.github.io/<repo>/`.

### From the command line instead

```bash
cd /Users/e.onorati/prototypes/balcony && git init -b main && git add -A && git commit -m "Balcony deck survey" && git remote add origin git@github.com:<user>/<repo>.git && git push -u origin main
```

Then set Settings → Pages as in step 3.

## About .nojekyll

GitHub Pages runs Jekyll by default, which ignores files and folders whose names
begin with `_` or `.`. Nothing here is named that way, so the site works without
`.nojekyll` — it is included only to skip the Jekyll step and deploy a little
faster. If the web uploader drops it, nothing breaks.

## Files

| Path | What it is |
|---|---|
| `index.html` | The whole page: markup, styles, and all the geometry code |
| `assets/balcony.spz` | The Gaussian splat, 693k splats with SH degree 1, in SPZ format (13 MB). Rendered with Spark |
| `assets/scan.bin` | 187,639 splat centres, quantised — position 3×uint16, colour 3×uint8. Shown as a quick point-cloud preview while `balcony.spz` downloads |
| `assets/horizon.jpg` | The site photos reprojected into one cylindrical panorama, 122° wide by 59° tall |
| `data/scene.json` | Terrain heightmap on a 12.5 cm grid, plus the door geometry |
| `data/levels.json` | Rock-face contour at 16 floor levels, for the height slider |
| `data/horizon.json` | Panorama bearing and elevation extents |
| `data/scan.json` | Point count and bounding box for dequantising `scan.bin` |
| `data/boards.json` | Decking options: board size, price and notes, for the cost table. `star_th` / `note_th` hold the Thai text |
| `dev.py` | Local server with live reload, for working on the page (not needed on Pages) |
| `renders/` | Photoreal views of the finished deck (not used by the page) |

## Notes

- **Must be served over http.** The page `fetch`es its data, so opening
  `index.html` straight off disk will show a message telling you so. For a local
  check: `python3 dev.py` in this folder, then open `http://localhost:8000/`.
  It reloads the page whenever a file changes. `dev.py` is only for local
  work and does not need to be uploaded.
- **External requests**: three.js 0.180 and Spark 2.3.1 (the splat renderer) from
  jsDelivr, via the import map at the top of `index.html`, and IBM Plex from
  Google Fonts. To make the site self-contained, download those and repoint the
  import map and the font `<link>`.
- **The splat** stays in the capture's own coordinate frame. `SPLAT_T` in
  `index.html` is the rigid transform from that frame into the survey's scan
  units; it was recovered by registering the original `balcony.ply` against
  `scan.bin` (residual 0.06 mm). `balcony.spz` was made from that PLY, cropped to
  20 units around the deck, with Spark's own SPZ encoder (`transcodeSpz`). The
  177 MB PLY is not in the repository — GitHub refuses files over 100 MB.
- **English and Thai.** The selector at the top right switches language in place;
  `?lang=th` opens the page in Thai directly, so that link can be shared. English
  text lives in the markup of `index.html`, Thai in the `TH` table in its script.
- **Shareable settings.** Moving a slider writes it to the URL — `depth`, `rw`, `rf`,
  `drop`, `scale`, `waste`, `bearing` — so a link opens the deck as configured,
  e.g. `?depth=3.5&rw=2&lang=th`. Values left at their default are omitted.
  Orbiting or zooming the 3D view adds `view=azimuth,elevation,distance`
  (degrees, degrees, metres), so the camera position is shared too.
- **Light and dark** follow the visitor's OS setting. There is no in-page toggle.
- All paths are relative, so the site works from a repository subpath without
  any configuration.
