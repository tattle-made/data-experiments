import argparse
import itertools
import json
import logging
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


START_TIME = time.time()
COUNTER = 1
ON_PROGRESS = True
PROCESS = None


class FacebookCommentScraper:
    def __init__(
        self, driver: webdriver.Chrome, url: str, averege_wait_time: int = 1
    ):
        self.driver = driver
        self.url = url
        self.averege_wait_time = averege_wait_time
        self.data = []
        logging.debug(f"Scraping comments from {url}")

    def __animate_loading(self, msg="Loading "):
        global ON_PROGRESS
        for c in itertools.cycle(["⠯", "⠟", "⠻", "⠽", "⠾", "⠷"]):
            if not ON_PROGRESS:
                break
            sys.stdout.write("\r" + msg + c)
            sys.stdout.flush()
            time.sleep(0.1)

    def scrape(self):
        global COUNTER, PROCESS
        PROCESS = threading.Thread(
            target=self.__animate_loading, args=(" 🔘 Scraping comments ",)
        )
        PROCESS.start()

        logging.debug(f"Loading animation started {self.url}")
        # Load page
        self.driver.get(self.url)
        logging.debug(f"Page loaded {self.url}")
        #print(f"Comments loaded {self.url}")
        #print(comments_link)
        #print('no')
        
        # Wait for comments to load
        try:
            comments_link = WebDriverWait(
            self.driver, self.averege_wait_time
            ).until(
             EC.presence_of_element_located(
                (By.XPATH, '//a[contains(., "comments")]')
                )
             )
        except:
            print(f"Comments loaded {self.url}")

        # Remove popup header
        container = self.driver.find_element_by_class_name("_5hn6")
        self.driver.execute_script(
            "arguments[0].style.display = 'none';", container
        )
        print(f"Popup header removed {self.url}")

        # Click on comments link
        self.driver.execute_script("arguments[0].click();", comments_link)
        print(
            f"Clicked on comments link {comments_link.text} {self.url}"
        )

        # Wait for comments to load
        commentFilter = WebDriverWait(
            self.driver, self.averege_wait_time
        ).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-ordering="RANKED_THREADED"]')
            )
        )
        logging.debug(f"Change comment filter {self.url}")

        # Click on comment filter
        self.driver.execute_script("arguments[0].click();", commentFilter)
        logging.debug(
            f"Clicked on comment filter {commentFilter.text} {self.url}"
        )

        # Wait for filter options to load
        self.driver.implicitly_wait(self.averege_wait_time)

        # Wait for filter options to load
        selectAllComment = self.driver.find_element(
            By.XPATH, '//div[starts-with(., "All comments")]'
        )
        logging.debug(f"Filter options loaded {self.url}")

        # Click on select `all comments` option
        self.driver.execute_script("arguments[0].click();", selectAllComment)
        logging.debug(f"Clicked on select all comments {self.url}")

        # Wait for comments to load
        self.driver.implicitly_wait(self.averege_wait_time)

        # Wait for comments to load and click on `... more comments` button
        try:
            while commentFilter := self.driver.find_element(
                By.XPATH, '//a[contains(., "more comments")]'
            ):
                self.driver.execute_script(
                    "arguments[0].click();", commentFilter
                )
                self.driver.implicitly_wait(self.averege_wait_time)
                logging.debug(f"Clicked on more comments {self.url}")
        except Exception as err:
            logging.info(err)

        # Wait for comments to load
        self.driver.implicitly_wait(self.averege_wait_time)
        logging.debug(f"Comments loaded {self.url}")

        # Get comments
        comments = self.driver.find_elements(
            By.CSS_SELECTOR, 'ul._7a9a > li [dir="ltr"]'
        )
        logging.debug(f"Comments scraped {self.url}")
        print(comments)

        # Click on `see more` button
        try:
            seeMore = self.driver.find_element(
                By.XPATH, '//a[contains(., "See More")]'
            )
            self.driver.execute_script("arguments[0].click();", seeMore)
            logging.debug(f"Clicked on see more {self.url}")
        except Exception as err:
            logging.info(err)

        for comment in comments:
            text = str(comment.get_attribute("innerText"))
            logging.debug(f"Comment scraped {text}")
            self.data.append({"text": text, "id": COUNTER})
            logging.debug(f"Comment added to data {text}")
            COUNTER += 1
            logging.debug(f"Counter increased {COUNTER}")

        print(f"\r✔️ {len(comments)} Comments scraped from {self.url}")
        return self.data


def main():
    global ON_PROGRESS, PROCESS
    # Process command line arguments
    parser = argparse.ArgumentParser(
        description="Process comment scraping from facebook post."
    )

    parser.add_argument(
        "urls", metavar="url", type=str, nargs="+", help="Facebook post url"
    )
    parser.add_argument(
        "-o", "--output", metavar="output", type=str, help="Output file name"
    )
    parser.add_argument(
        "-l", "--log", metavar="log", type=str, help="Log level"
    )

    args = parser.parse_args()

    # Setup logging
    if args.log is not None:
        logging.basicConfig(level=args.log.upper())

    # Setup selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--headless")
    options.add_extension("./extension_1_0_4_0.crx")
    logging.debug("Extension added to webdriver")

    driver = webdriver.Chrome(
        options=options,
        executable_path=(
            "./chromedriver"
            if sys.platform == "linux"
            else "./chromedriver.exe"
        ),
    )
    logging.debug("Webdriver started")

    # Scrape comments
    datas = []

    for url in args.urls:
        try_count = 0
        while try_count < 3:
            try:
                scraper = FacebookCommentScraper(driver, url, 5)
                datas += scraper.scrape()
                logging.debug(f"Comments scraped from {url}")
                break
            except Exception as err:
                logging.info(err)
                try_count += 1

    if args.output is not None:
        logging.debug(f"Output file {args.output}")
        with open(args.output, "w") as f:
            json.dump(datas, f, indent=2)
            logging.debug(f"Data written to file {args.output}")
    else:
        sys.stdout.write(json.dumps(datas, indent=2))
        logging.debug("Data written to stdout")

    driver.quit()
    logging.debug("Webdriver closed")

    ON_PROGRESS = False
    PROCESS.join()
    STOP_TIME = time.time()
    print("\r✨✨ Scraping Done! ✨✨")
    # Create table for time elapsed and total comments scraped
    print(
        f"{'-' * 40}\n{'💠 Total Comments ':<25}|{COUNTER-1:>5}\n{'-' * 40}\n"
        f"{'⏰ Time Elapsed (Min)':<25}|{(STOP_TIME - START_TIME)/60:.>2f}"
        f"\n{'-' * 40}"
    )


if __name__ == "__main__":
    main()
