# YYeTs_db

Sqlite3 database of YYeTs.

`Across the Great Wall we can reach every corner in the world.`

[toc]

## About The Project

![Product Name Screen Shot](./images/screenshot.png)

YYeTs has been shut down for some reason. So I parsed download links and saving to database from raw data. You can now search with SQL and download movies with the link you got. The links are still available **for now**. 

Why sqlite:

* Offline. You can search without network so that no one can "shut down" your "sql server".
* Easy. No need to install python package for sql driver. Python has built-in sqlite module since python 2.5.x.

The cost is that you should download the whole database first (30M+ zip, 220M+ disk space).

## Usage

### Database

1. download latest release
2. unzip
3. open with sqlite3
4. search url with SQL

### Python cli

#### Prerequisites

1. [download database](#Database) and unzip (yyets.db)
2. python3 (test in 3.8 and 3.9)
3. set pip mirror source at https://mirrors.tuna.tsinghua.edu.cn/help/pypi if are inside the GreatWall

#### Install

1. Clone the repo

   ``` sh
    git clone https://github.com/Piiikachu/YYeTs_db.git
   ```

2. ~~Install dependencies~~ (skip this step for now)

   ``` sh
    pip install -r requirement.txt
   ```

3. run cli.py

   ``` sh
    python ./cli.py
   ```

#### Settings

1. set path to yyets.db
2. start searching

## TBD

* [x] upload tool script.
* [x] update readme.md.
* [ ] upgrade searching strategy. For now the searching is using `Left-Prefix Index Rule` for efficiency.
* [x] user interface with python CLI.
* [ ] multi-selection.
* [ ] auto paste to clipboard.
* [ ] TUI/GUI.

## Credits

Thanks for the data source.
[@BennyThink](https://github.com/BennyThink)
