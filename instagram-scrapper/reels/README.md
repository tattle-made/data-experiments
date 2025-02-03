## Reels Scrapper
The code is just a jupyter notebook, one can simply install the packages and run the jupyter notebook anyway they want. 

### Recommned way to Run it

1. [install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

2. create a venv (and activate)
```sh
uv venv
source .venv/bin/activate
```

3. install jupyter notebook and other related dependencies
```
uv pip install -r requirements.txt
```

4. create a `.env` and add your instagram username and password. The env file should have the following variables. 
```sh
INSTA_USERNAME=
INSTA_PASSWORD=
```
5. The code use's firefox and hence depends on the `geckodriver`. Install the geckodriver based on your system from [here](https://github.com/mozilla/geckodriver/releases). Then replace the path with your system path where the geckodriver is stored in the code. 

6. run the jupyter notebook
```sh
jupyter notebook
```

7. The code does NOT have the function to run for `N` amount of time. Instead we have to pass the number of reels we want to scrape along with some delay in the `scrape_reels_links()` function. 
   - recommneded delay is of 0.5 seconds.
   - say you want to keep the scrapper running for 1 hour, then you pass number of reels to the function to be 7200 with a dealy of 0.5 seconds.