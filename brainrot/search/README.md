# Search Notebooks

Purpose: build a FAISS index over CLIP embeddings and run text→video search; inspect zero-shot labels via thumbnails.

## Prerequisites
- Ensure `analysis/02_extract_video_embeddings.ipynb` has produced `video_data_2.pkl` (or compatible `.pkl` with embeddings and metadata).
- Activate the environment (see root `README.md`).

## Notebooks
1. `01_index_video_files.ipynb`
  - What it does: Loads embeddings from one or more `.pkl` files, creates a FAISS index (Inner Product on L2-normalized vectors), and saves index artifacts.
  - Inputs: `PKL_FILES_DIRECTORY` pointing to folder with files like `video_data_2.pkl`.
  - Outputs: `faiss_index/video_index.faiss`, `faiss_index/video_metadata.pkl`, `faiss_index/index_info.txt`.

2. `02_search_videos.ipynb`
  - What it does: Loads FAISS index and metadata; encodes a text query with CLIP and retrieves top-k nearest videos; provides grid and clickable thumbnail display helpers.
  - Inputs: `faiss_index/` directory from the previous notebook; internet for model weights if not cached.
  - Outputs: Interactive visualization in the notebook; no files written.

3. `03_show_auto_labelling.ipynb`
  - What it does: Loads `video_tsne_enriched_data_viz_without_base64.json` and displays thumbnails grouped by zero-shot prediction label; prints counts per label.
  - Inputs: `video_tsne_enriched_data_viz_without_base64.json` (from analysis step) with valid `thumbnail_path` and `video_path`.
  - Outputs: Interactive grouping display; no files written.

## Data Flow Summary
`video_data_2.pkl` → 01_index_video_files → `faiss_index/*` → 02_search_videos for querying. Separately, enriched JSON from analysis feeds 03_show_auto_labelling.

