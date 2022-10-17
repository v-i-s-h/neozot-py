"""
    Neozot
"""

import os
import argparse
import logging
from datetime import datetime

from zoterodb import ZoteroDB
from feedprovider import ArxivFeedProvider
from recommender import Recommender

import jinja2


def main():
    parser = argparse.ArgumentParser(
        prog="neozot", description="Super charge your zotero"
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

    arxiv = ArxivFeedProvider(domains=arxivdomains)
    feed = arxiv.get_feed_summary(force_refresh=force_refresh)
    # display_items(feed)

    rec = Recommender()
    suggested_items = rec.get_recommendations(library, feed, K=20)

    # Write out to html file
    timestamp = datetime.now().strftime("%Y-%m-%d")
    outfile = os.path.join("feeds", timestamp, args.outfile)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    template = env.get_template("results.html")

    content = template.render({"feeditems": suggested_items})
    with open(outfile, mode='w', encoding='utf-8') as f:
        f.write(content)
    


def display_items(library):
    for i, (id, info) in enumerate(library.items()):
        buffer = "{:4d}\n".format(i)
        buffer += "        id              : {}\n".format(id)
        for k, v in info.items():
            buffer += "        {:16s}: {}\n".format(k, v)
        print(buffer)





if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    main()
