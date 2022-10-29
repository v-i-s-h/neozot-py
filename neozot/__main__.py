"""
    Neozot
"""

import os
import argparse
import logging
import json

import appdirs
import eel

from .zoterodb import ZoteroDB
from .feedprovider import ArxivFeedProvider
from .recommender import Recommender


def load_update_pref(pref_file, prefs_given):
    """
        load_update_pref
        Loads and updates the preferences based on given preference options

    Inputs:
        pref_file - json file path where the preferences are stored
        prefs_given - Preference given by the user, as a dictionary

    Returns:
        preferences with missing updated from file

    """

    # Hard code defaults
    prefs = {
        'domains': ['cs'],
        'n_items': 10,
    }

    # Bit cleaning to avoid wrong updates
    ## 1. if zotdir is not given, remove key
    if 'zotdir' in prefs_given and prefs_given['zotdir'] is None:
        del prefs_given['zotdir']
    ## 2. if no domains are given, remove key
    if 'domains' in prefs_given and prefs_given['domains'] is None:
        del prefs_given['domains']
    ## 3. if n_items is None (on first page load), remove key
    if 'n_items' in prefs_given and prefs_given['n_items'] is None:
        del prefs_given['n_items']

    # Load preference from file if exists
    if os.path.exists(pref_file):
        with open(pref_file, mode='r') as pref_json:
            saved_prefs = json.load(pref_json)
        prefs.update(saved_prefs)
    
    # Update with preference overides
    updated = False
    for k, v in prefs_given.items():
        if k not in prefs or prefs[k] != v: # Check if saved value is not same as given
            # logging.info("Updated {} --- {}".format(k, v))
            prefs[k] = v
            updated = True # Mark as updated preferences

    if updated:
        with open(pref_file, 'w') as pref_json:
            # logging.info("Writing changes to preferences")
            json.dump(prefs, pref_json)

    return prefs


def main():
    parser = argparse.ArgumentParser(
        prog="neozot", description="Super charge your research"
    )
    parser.add_argument(
        "--zotdir", help="Data directory of Zotero", type=str
    )
    parser.add_argument(
        "-d",
        "--domains",
        help="""arxiv domain(s) to search in """
        """(Ex: cs.LG cs.CV cs.AI or high level as cs, math etc)""",
        nargs="+",
        default=None
    )
    parser.add_argument(
        "--n-items", type=int, default=None,
        help="Number of items to suggest by default"
    )
    parser.add_argument("-f", "--force-refresh", action="store_true")
    # parser.set_defaults(force_refresh=False)
    args = parser.parse_args()
    
    # Load/Save/Update config
    appdir = appdirs.AppDirs(appname="neozot", appauthor="neozot")
    os.makedirs(appdir.user_config_dir, exist_ok=True)
    os.makedirs(appdir.user_cache_dir, exist_ok=True)
    preferences_json = os.path.join(appdir.user_config_dir, "prefs.json")
    neozot_db = os.path.join(appdir.user_cache_dir, "neozot.sqlite")
    prefs = load_update_pref(preferences_json, vars(args))

    if 'zotdir' not in prefs:
        # zot dir is not configured,
        # looks like first run, ask user to give Zotero data directory
        print("Looks like neozot is not configured yet")
        print("Please run neozot with '--zotdir <Zotero data directory>")
        return # Exit from main

    zotdir = prefs['zotdir']
    force_refresh = prefs.get('force_refresh', False)
    
    zotdb = ZoteroDB(zotdir)
    library = {}  # We will load after UI appears
    # display_items(library)

    @eel.expose
    def get_arxiv_suggestions(domains, n_items):
        nonlocal library
        
        # update prefs if required
        _prefs = load_update_pref(preferences_json, {
            'domains': domains,
            'n_items': n_items
        })

        # Error check
        domains = _prefs['domains']
        n_items = _prefs['n_items']

        if not library:
            # If library is not loaded yet, then load
            library = zotdb.get_library()

        arxiv = ArxivFeedProvider(domains=domains)
        feed = arxiv.get_feed_summary(force_refresh=force_refresh)

        rec = Recommender()
        suggested_items = rec.get_recommendations(library, feed, K=n_items)

        return n_items, domains, suggested_items

    @eel.expose
    def get_feed_items(domains):
        # Get all items from feeds
        arxiv = ArxivFeedProvider(domains=domains)
        feed = arxiv.get_feed_summary(force_refresh=force_refresh)

        return feed

    eel.init("neozot/ui")
    eel.start("")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
