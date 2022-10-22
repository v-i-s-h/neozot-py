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
    )
    parser.add_argument("-f", "--force-refresh", action="store_true")
    parser.set_defaults(force_refresh=False)
    parser.add_argument("-o", "--outfile", default="feed.html")
    args = parser.parse_args()

    datadir = args.datadir
    arxivdomains = args.domains
    force_refresh = args.force_refresh

    zotdb = ZoteroDB(datadir)
    library = zotdb.get_library()
    # display_items(library)

    @eel.expose
    def get_arxiv_suggestions():
        arxiv = ArxivFeedProvider(domains=arxivdomains)
        feed = arxiv.get_feed_summary(force_refresh=force_refresh)
        # display_items(feed)

        rec = Recommender()
        suggested_items = rec.get_recommendations(library, feed, K=5)

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
