# Brainrot Analysis

This repository contains experiments analyzing Instagram reels. We collected ~1500 reels from our instagram feed and wanted to look at what does one see on their feed? what goes around on instagram? is there a way through which we can find how much of the data is brainrot?

- [`analysis/`](https://github.com/tattle-made/data-experiments/tree/master/brainrot/analysis): Code to preprocess videos, extract embeddings, cluster, and prepare data for visualization.
- [`visualisation/`](https://github.com/tattle-made/data-experiments/tree/master/brainrot/visualisation): Standalone HTML/CSS/JS visualizations to explore the clustered data and labels.
- [`search/`](https://github.com/tattle-made/data-experiments/tree/master/brainrot/search): Notebooks to build a simple embeddings index and run vector search over the videos.

Each folder includes its own README with per-file inputs/outputs and usage details:

- See [`analysis/README.md`](https://github.com/tattle-made/data-experiments/blob/master/brainrot/analysis/README.md)
- See [`visualisation/README.md`](https://github.com/tattle-made/data-experiments/blob/master/brainrot/visualisation/README.md)
- See [`search/README.md`](https://github.com/tattle-made/data-experiments/blob/master/brainrot/search/README.md)

## Recommned way to run the code

1. [install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

2. create a venv (and activate)
```sh
uv venv
source .venv/bin/activate
```

3. install jupyter notebook and other related dependencies
```sh
uv pip install -r requirements.txt
```

4. start the jupyter notebook environment
```sh
jupyter notebook
```

## Some files will need more setup
You will have to login to instagram for some code to collect reels, for that do the following

- create a `.env` and add your instagram username and password. The env file should have the following variables. 
```sh
INSTA_USERNAME=
INSTA_PASSWORD=
```
- The code use's firefox and hence depends on the `geckodriver`. Install the geckodriver based on your system from [here](https://github.com/mozilla/geckodriver/releases). Then replace the path with your system path where the geckodriver is stored in the code. 

## Data expectations at a glance
- Raw videos (e.g., `.mp4`) organized by day or source directory.
- Generated artifacts during analysis: `video_data_2.pkl`, optional `video_embeddings.npy`, and `visualisation/video_tsne_enriched_data_viz_without_base64.json`.
- Visualizations expect the enriched JSON above and access to thumbnails/videos via paths embedded in the JSON or via a predictable base URL (see each visualization README).