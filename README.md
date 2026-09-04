# Balcony Deck Survey

A static site. Deck geometry measured from a Gaussian splat of the balcony:
interactive 3D model, dimensioned plan, section, clearance table, and a
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
cd /Users/e.onorati/balcony && git init -b main && git add -A && git commit -m "Balcony deck survey" && git remote add origin git@github.com:<user>/<repo>.git && git push -u origin main
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
| `assets/scan.bin` | 187,639 splat points, quantised — position 3×uint16, colour 3×uint8 |
| `assets/horizon.jpg` | The site photos reprojected into one 122° cylindrical panorama |
| `assets/skirt.jpg` | Colour ramp that carries the panorama down to the ground |
| `assets/photo-p*.jpg` | The five site photos, for the gallery |
| `data/scene.json` | Terrain heightmap on a 12.5 cm grid, plus the door geometry |
| `data/levels.json` | Rock-face contour at 16 floor levels, for the height slider |
| `data/horizon.json` | Panorama bearing and elevation extents |
| `data/scan.json` | Point count and bounding box for dequantising `scan.bin` |
| `data/photos.json` | Per-photo compass heading, focal length and caption |

## Notes

- **Must be served over http.** The page `fetch`es its data, so opening
  `index.html` straight off disk will show a message telling you so. For a local
  check: `python3 -m http.server` in this folder, then open
  `http://localhost:8000/`.
- **Two external requests**: three.js r128 from cdnjs, and IBM Plex from Google
  Fonts. To make the site fully self-contained, download those and repoint the
  two `<link>`/`<script>` tags at the top of `index.html`.
- **Light and dark** follow the visitor's OS setting. There is no in-page toggle.
- All paths are relative, so the site works from a repository subpath without
  any configuration.
