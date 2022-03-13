# Reddit
![](https://heroku-status-badges.herokuapp.com/bereddit-dash)
![](https://img.shields.io/badge/python-v3.7.12-blue)
[![](https://img.shields.io/badge/license-MIT-blue)](https://github.com/reddit-conflicting-viewpoints/Reddit/blob/main/LICENSE)

**By: Andrew Zhou, Sai Muktevi, Preston Stringham, Hasnah Said**


Web Visualization Dashboard can be found [here](http://bereddit-dash.herokuapp.com/).

## Installation and Setup
This tutorial will allow you to run the code locally on your own machine!  
*It is recommended that you create a new conda environment (if you have conda) or a new virtual environment before installation.*

1) Clone the git repository to your local machine and change directory to recipeat
```
git clone https://github.com/reddit-conflicting-viewpoints/Reddit.git
cd Reddit
```
2) Install required packages and dependecies. This installs from our `setup.py` file.
```
pip install -r requirements.txt
```
3) You're ready to start running our app locally!  

* Run dash application
```
python app.py
```
* Run the scraper
```
python src/data/scraper.py
```
Note: scraper.py has the following arguments:  
1) Subreddit: '-s' or '--subreddit'. The subreddit to scrape from. Will scrape 'computerscience' by default.

2) Order: '-o' or '--order'. The order the scraper will scrape from. Will scrape 'hot' by default.

3) Maximum Post: '-mp' or '--maxpost'. The maximum number of posts the scraper can scrape. 1000 by default 

4) Maximum Comment Post: '-mcp' or '--maxcommentpost'. The maximum number of comments that can be scraped per post. 100 by default

5) Maximum Comment: '-mc' or '--maxcomment'. The maximum number of comments the scraper can scrape. 10000 by default. Note: The scraper may go over 10000 by a little bit

* Run BERT for topic modeling, sentiment analysis, and relevance analysis
```
python src/models/subreddit_analysis.py
```
Note: This module has to be run after scraper.py. subreddit_analysis.py has the following arguments:  
1) Subreddit: '-s' or '--subreddit'. The subreddit to analyze from. Will analyze 'computerscience' by default.

2) Order: '-o' or '--order'. The order the scraper had scraped from. 'hot' by default.

3) Maximum Post: '-mp' or '--maxpost'. The maximum number of posts to analyze. 2000 by default 

4) Maximum Comment: '-mc' or '--maxcomment'. The maximum number of comments to analyze. 20000 by default.

## Data Handling

### Downloading data
```
make data
```

```
python src/data/scraper.py
```
Recommended running `python src/data/scraper.py` as this allows argument parsing.  

Files will be downloaded to data/raw/.

### Syncing your data to azure blob
```
make sync_data_to_blob
```
Files in data/ will be synced to azure blob.

### Syncing your data from azure blob
```
make sync_data_from_blob
```
Fetch files in azure blob to your local machine. Note: If you have a file with the same name on azure blob, those files will not sync.  
Example: computerscience_comments.csv is on your local machine, and a new version of computerscience_comments.csv is on azure blob. The new version of computerscience_comments.csv on azure blob will not replace the local copy. 
