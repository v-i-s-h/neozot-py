"""
    Neozot
"""

import argparse
import logging

import eel

from .zoterodb import ZoteroDB
from .feedprovider import ArxivFeedProvider
from .recommender import Recommender


def main():    
    parser = argparse.ArgumentParser(
        prog="neozot", description="Super charge your research"
    )
    parser.add_argument("datadir", help="Data directory of Zotero", type=str)
    parser.add_argument(
        "-d",
        "--domains",
        help="""arxiv domain(s) to search in """
        """(Ex: cs.LG cs.CV cs.AI or high level as cs, math etc)""",
        nargs="+",
        default=['cs']
    )
    parser.add_argument("-f", "--force-refresh", action="store_true")
    parser.set_defaults(force_refresh=False)
    args = parser.parse_args()

    datadir = args.datadir
    arxivdomains = args.domains
    force_refresh = args.force_refresh

    zotdb = ZoteroDB(datadir)
    library = None # We will load after UI appears
    # display_items(library)

    @eel.expose
    def get_arxiv_suggestions(domains, n_items=5):
        print("Request: ", domains, n_items)
        nonlocal library
        if library is None:
            # If library is not loaded yet, then load
            library = zotdb.get_library()
        
        arxiv = ArxivFeedProvider(domains=domains)
        feed = arxiv.get_feed_summary(force_refresh=force_refresh)
        # display_items(feed)

        rec = Recommender()
        suggested_items = rec.get_recommendations(library, feed, K=n_items)

        return suggested_items

    eel.init("neozot/ui")
    eel.start("index.html")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
