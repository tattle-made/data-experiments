# Visualisation (HTML/CSS/JS)

Purpose: interactive D3-based visualizations for exploring t-SNE embeddings, clusters, days, and zero-shot labels. These pages read the enriched JSON exported by analysis and expect access to thumbnails and video files.

## Prerequisites
- Generate `video_tsne_enriched_data_viz_without_base64.json` via `analysis/04_video_tsne_cluster.ipynb` (and optionally updated by `analysis/05_rasterfairy.ipynb`).
- Ensure thumbnails exist at `thumbnails/<video_id>.jpg` and videos at `video_reels/<video_id>.mp4`, or adjust the `imageBaseURL` / `videoBaseURL` in each file.
- Serve these HTML files with a static server from the `visualisation/` directory if local file access blocks `fetch` (e.g., `python -m http.server`).

## Setup
- setup a http server in the folder
- make sure `video_reels/` and `thumbnails/` folders are in this folder
- then run a http server using `uv` like this:
```sh
uv run -m http.server 8000
```

## Files
1. `01_scrolling_better_viz.html`
  - What it does: Plays short video previews sequentially and places their thumbnails at t-SNE positions; supports zoom/pan and skip-to-end to render all thumbnails.
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json`; thumbnails and videos via `imageBaseURL`=`thumbnails/`, `videoBaseURL`=`video_reels/`.
  - Outputs: Visual interaction only.

2. `02_tsne_countour_multi_day_filter.html`
  - What it does: Renders t-SNE points with multi-day filtering controls; displays contours and supports toggling clusters/days (see UI controls).
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json`; thumbnails/videos via base URLs defined inside the file.
  - Outputs: Visual interaction only.

3. `03_zero_shot_prediction.html`
  - What it does: Groups thumbnails by zero-shot prediction label; interactive day filter and label grouping.
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json`; thumbnails/videos expected via base URLs in the file.
  - Outputs: Visual interaction only.

4. `04_toggle_preview_mode.html`
  - What it does: Switches between dot mode and thumbnail preview mode; supports filter by day and active label (cluster or zero-shot) with toggles for mute/labels.
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json`; thumbnails/videos via `config.imageBaseURL` and `config.videoBaseURL` in the script.
  - Outputs: Visual interaction only.

5. `05_rasterfairy.html`
  - What it does: Displays thumbnails arranged on a RasterFairy-aligned grid using `rasterfairy_coordinates` added by the analysis notebook.
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json` including `rasterfairy_coordinates`; uses `payload.thumbnail_path` for images.
  - Outputs: Visual interaction only.

Data File Schema (enriched JSON)
Each entry example (simplified):
```
{
  "payload": {
    "video_id": "<id>",
    "video_path": ".../video_reels/<id>.mp4",
    "thumbnail_path": "thumbnails/<id>.jpg",
    "day": <int>,
    "zero_shot_prediction": "<label>",
    "cluster": "<cluster_id>"
  },
  "reduced_embedding": [x, y],
  "reduced_embedding_normalized": [0..1, 0..1],
  "cluster": "<cluster_id>",
  "rasterfairy_coordinates": [gridX, gridY] // if added
}
```

