# Reddit
[![](https://heroku-status-badges.herokuapp.com/bereddit-dash)](http://bereddit-dash.herokuapp.com/)
![](https://img.shields.io/badge/python-v3.7.12-blue)
![](https://img.shields.io/badge/license-MIT-blue)

Reddit project

Web Visualization Dashboard can be found [here](http://bereddit-dash.herokuapp.com/).

### Installing development requirements

```
pip install -r requirements.txt
```

### Running tests
```
py.test tests
```
# Data Handling

### Downloading data
```
make data
```
Files will be downloaded to data/raw/

### Syncing your data to azure blob
```
make sync_data_to_blob
```
Files in data/ will be synced to azure blob

### Syncing your data from azure blob
```
make sync_data_from_blob
```
Fetch files in azure blob to your local machine. Note: If you have a file with the same name on azure blob, those files will not sync.  
Example: computerscience_comments.csv is on your local machine, and a new version of computerscience_comments.csv is on azure blob. These files will not sync.  
Had issues trying to resolve this.
