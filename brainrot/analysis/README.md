# Analysis Notebooks

Purpose: preprocess raw reels, extract visual embeddings with CLIP, compute t-SNE and clusters, enrich payloads with labels and day info, and produce JSON for visualizations.

## Prerequisites
- Activate the project environment (see root `README.md`).
- Required data: a folder containing `.mp4` videos; write paths in the first cells where applicable.

## Notebooks
1. `01_find_time_of_data.ipynb`
  - What it does: Scans a folder of `.mp4` files with `ffmpeg` to compute duration and file size; summarizes totals.
  - Input: `folder` path to videos (e.g., `/path/to/video_reels`).
  - Output: `video_durations.json` with per-video `{duration_seconds, size_mb}` and console stats.

2. `02_extract_video_embeddings.ipynb`
  - What it does: Extracts I-frames per video, runs CLIP (`openai/clip-vit-base-patch32`) to compute an average embedding, saves a thumbnail and metadata per video.
  - Input: `folder_path` with `.mp4` files; GPU optional but recommended; creates `thumbnails/`.
  - Output: `video_data_2.pkl` (list of dicts: `video_id, video_path, embedding, thumbnail_path`). Optionally `video_embeddings.npy` if you enable that cell.

3. `03_load_pickle_data.ipynb`
  - What it does: Quick loader/inspector for `video_data_2.pkl` and optional `video_embeddings.npy`; previews thumbnail and checks embedding dims.
  - Input: `video_data_2.pkl` (and optionally `video_embeddings.npy`).
  - Output: None (interactive inspection only).

4. `04_video_tsne_cluster.ipynb`
  - What it does: Uses Feluda operators to run t-SNE dimensionality reduction and clustering over embeddings; enriches payload with `day`, `cluster`, and zero-shot label using CLIP text features; normalizes coordinates.
  - Input: `video_data_2.pkl`; a `base_dir` containing per-day folders like `day1/`, `day2/` with `.mp4` files to infer `day`; label list in the notebook for zero-shot.
  - Output: `video_tsne_enriched_data_viz_without_base64.json` containing `[ { payload: {video_id, video_path, thumbnail_path, day, zero_shot_prediction, cluster}, reduced_embedding, reduced_embedding_normalized, cluster } ]`.

5. `05_rasterfairy.ipynb`
  - What it does: Loads the enriched JSON, computes a grid-aligned layout via RasterFairy, and writes back `rasterfairy_coordinates` for each item.
  - Input: `visualisation/video_tsne_enriched_data_viz_without_base64.json` produced by the previous notebook.
  - Output: Updates the same JSON in place, adding `rasterfairy_coordinates`.

## Data Flow Summary
videos (.mp4) → 02_extract_video_embeddings → `video_data_2.pkl` → 04_video_tsne_cluster → `video_tsne_enriched_data_viz_without_base64.json` → 05_rasterfairy augments JSON → visualisation.