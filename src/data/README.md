0. ensure conda is already installed on your computer
1. navigate to downloaded and unzipped filefolder and from terminal run: conda create -f uwmsds.yml
2. run: conda activate uwmsds && sudo chmod +x scrape_reddit.sh && ./scrape_reddit.sh
3. after scraping, the data will in ./data folder as csv files
4. modify config.py to change scraper settings (e.g. which subreddit, how many posts etc)
