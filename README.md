# neozot
neozot is a utility to get recommendations from arxiv based on your zotero library.

![as](./imgs/neozot.png)

neozot will list the matching preprints from arxiv along with the closest match it
found in your zotero library and the score. By default, it lists 20 top suggestions.

## Usage
```
usage: neozot [-h] [-d DOMAINS [DOMAINS ...]] [-f] datadir

Super charge your research

positional arguments:
  datadir               Data directory of Zotero

options:
  -h, --help            show this help message and exit
  -d DOMAINS [DOMAINS ...], --domains DOMAINS [DOMAINS ...]
                        arxiv domain(s) to search in (Ex: cs.LG cs.CV cs.AI or high level as cs, math etc)
  -f, --force-refresh
```
Example

1. If you zotero library is in `~/Zotero/` (directory where `zotero.sqlite` is stored) and you
want to get arxiv recommendations from `cs` domain, then use
```bash
python -m neozot ~/Zotero/ -d cs
```
OR
```bash
python -m neozot ~/Zotero/ 
```
2. If you only want results from `cs.AI` and `cs.LG`, use
```bash
python -m neozot ~/Zotero/ -d cs.AI cs.LG
```

By default, neozot will suggest top 5 items from `cs` domain. You can adjust this
by using `Settings` from the sidebar.

The options in UI sidebar are
|Icon|Description|
|:-|:-|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/inbox.svg" width="24" height="24">|**Suggestions**: Top suggestion from today's arxiv feed based on your Zotero items|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/compass.svg" width="24" height="24">|**Explore**: Show all feed items from arxiv|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bookmark.svg" width="24" height="24">|**Bookmarked**: *Not Implemented*|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/github.svg" width="24" height="24">|**Github**: Visit github repo|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" width="24" height="24">|**Settings**: Select arxiv domains to follow, number of items to suggest etc|

## Requirements
1. [eel](https://pypi.org/project/Eel/) (>= 0.14.0)
2. [scikit-learn](https://pypi.org/project/scikit-learn/) (>= 1.0.1)
3. [requests](https://pypi.org/project/requests/) (>= 2.27.1)

PS: Version suggestions are verions against which neozot is developed.
