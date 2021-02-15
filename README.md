# README

This will bring back the JSON data from Hamrobazar.

## How to install?

### Step 1 - Install Python

[https://www.python.org/downloads/](https://www.python.org/downloads/)

### Step 2 - Install the dependencies

Method 1  
Install all packages from requirements.txt
`sudo apt update`
`sudo apt install python3-pip`
`pip3 install -r requirements.txt`
or
`pip install -r requirements.txt`

Method 2  
Install the each packages one by one

- `pip install BeautifulSoup`
- `pip install requests`
- etc.

## Set project-algorithm folder as python path

## In unix

    export PYTHONPATH=`pwd`

## In Windows

    set PYTHONPATH=.

`python 1-categoryCrawler/CategoryCrawler.py`

## In Power Shell

`$env:PYTHONPATH='path\to\base-folder`

Eg:
`cd D:\Code\personal\project\project-algorithm`
`$env:PYTHONPATH='D:\Code\personal\project\project-algorithm`

## To check the list of existing dependencies

`pip list`
