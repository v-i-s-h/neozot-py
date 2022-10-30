# neozot
neozot is a utility to get recommendations from arxiv based on your zotero library.

![neozot](./imgs/neozot.png)

## Install
### Using PyPI
```
pip install neozot
```

### From repository
1. Clone this repository using
```
git clone https://github.com/v-i-s-h/neozot-py.git
```
2. Install using
```bash
pip install .
```
3. If you want to install in developer/editable mode,
```
pip install -e .
```

## Usage
To run neozot, you can
```
python -m neozot
```
#### First run
On first run, you are required to provide the path of Zotero data directory as
```
python -m --zotdir <path-to-zotero-data-dir>
```
Example:
```
python -m neozot --zotdir ~/Zotero/
```
Same can all be used to change the path to Zotero data directory later.

Additionally, neozot can also be configured with a couple of options through CLI. 
Full command line options are
```
usage: neozot [-h] [--zotdir ZOTDIR] [-d DOMAINS [DOMAINS ...]] [--n-items N_ITEMS] [-f]

Super charge your research

options:
  -h, --help            show this help message and exit
  --zotdir ZOTDIR       Data directory of Zotero
  -d DOMAINS [DOMAINS ...], --domains DOMAINS [DOMAINS ...]
                        arxiv domain(s) to search in (Ex: cs.LG cs.CV cs.AI or high level as cs, math etc)
  --n-items N_ITEMS     Number of items to suggest by default
  -f, --force-refresh

```
Examples

1. If you zotero library is in `~/Zotero/` (directory where `zotero.sqlite` is stored) and you
want to get arxiv recommendations from `cs` and `math` domains, then use
```bash
python -m neozot --zotdir ~/Zotero/ -d cs math
```
2. If you only want results from `cs.AI` and `cs.LG`, use
```bash
python -m neozot --zotdir ~/Zotero/ -d cs.AI cs.LG
```

The options in UI sidebar are
|Icon|Description|
|:-|:-|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/inbox.svg" width="24" height="24">|**Suggestions**: Top suggestion from today's arxiv feed based on your Zotero items|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/compass.svg" width="24" height="24">|**Explore**: Show all feed items from arxiv|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/bookmark.svg" width="24" height="24">|**Bookmarked**: *Not Implemented*|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/github.svg" width="24" height="24">|**Github**: Visit github repo|
|<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gears.svg" width="24" height="24">|**Settings**: Select arxiv domains to follow, number of items to suggest etc|

