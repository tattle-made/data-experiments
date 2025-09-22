# Code to Extract DAU Quaterly report data

## Recommned way to Run it

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
- you can also generate/re-compile the file like this `uv pip compile requirements.in -o requirements.txt`

4. Start the jupyter notebook environment like this
```sh
jupyter notebook
```

## Input data
- the code expects the dump of feed common table from DAU Dashboard