"""
    Neozot
"""

import argparse
import json

from zoterodb import ZoteroDB
from feedprovider import ArxivFeedProvider

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel as similarity


def main():
    parser = argparse.ArgumentParser(
        prog="neozot", description="Super charge your zotero"
    )
    parser.add_argument("datadir", help="Data directory of Zotero", type=str)
    parser.add_argument(
        "-d",
        "--domains",
        help="arxiv domain to search in (ex: cs.LG, cs.CV, cs.AI etc",
        nargs="+",
    )
    parser.add_argument("-f", "--force-refresh", action="store_true")
    parser.set_defaults(force_refresh=False)
    args = parser.parse_args()
    print(args)

    datadir = args.datadir
    arxivdomains = args.domains
    force_refresh = args.force_refresh

    zotdb = ZoteroDB(datadir)
    library = zotdb.get_library()
    # display_items(library)

    arxiv = ArxivFeedProvider(domains=arxivdomains)
    feed = arxiv.get_feed_summary(force_refresh=force_refresh)
    # display_items(feed)

    # Build a summary of each item, only if it has abstract
    items_summary = build_summary(library)
    print(
        "Created summary for {}/{} documents.".format(len(items_summary), len(library))
    )

    feed_summary = build_summary(feed)
    print("Created summary for {}/{} feed items.".format(len(feed_summary), len(feed)))

    # Create feature builder
    encoder = TfidfVectorizer(
        input="content",
        strip_accents="unicode",
        lowercase=True,
        analyzer="word",
        stop_words="english",
        max_df=0.20,
        min_df=0.02,
        norm="l2",
        use_idf=True,
    )

    items_embedding = encoder.fit_transform(items_summary.values())
    feed_embedding = encoder.transform(feed_summary.values())

    feed_similarity = similarity(items_embedding, feed_embedding)

    # Get top K pairs
    # Ref: https://stackoverflow.com/a/57105712
    K = 10
    top_K = np.c_[
        np.unravel_index(
            np.argpartition(feed_similarity.ravel(), -K)[-K:], feed_similarity.shape
        )
    ]

    # Index to id mapping for library
    ids_library = list(items_summary.keys())
    # For feed, the key itself can be index, but just creating the map
    ids_feed = list(feed_summary.keys())

    for i, j in top_K:
        item_id = ids_library[i]
        feed_id = ids_feed[j]

        print(library[item_id])
        print(feed[feed_id])
        print("Score: ", feed_similarity[i, j], i, j)
        print("----")

    # Print feed similarity
    n_feed = len(feed_summary)
    n_items = len(items_summary)
    for i, (id, info) in enumerate(library.items()):
        print("{:3d}. {}".format(i + 1, info["title"]))
    for i, (id, info) in enumerate(feed.items()):
        print("{:3d}.        ".format(i + 1), end="")
        for j in range(n_items):
            print("{:.4f}    ".format(feed_similarity[j, i]), end="")
        print("{:120s}  {:30s}".format(info["title"], info["link"]))


def display_items(library):
    for i, (id, info) in enumerate(library.items()):
        buffer = "{:4d}\n".format(i)
        buffer += "        id              : {}\n".format(id)
        for k, v in info.items():
            buffer += "        {:16s}: {}\n".format(k, v)
        print(buffer)


def build_summary(library):
    summary = {}
    for id, info in library.items():
        _title = info.get("title", None)
        _abstract = info.get("abstractNote", None)
        if _title and _abstract:
            summary[id] = _title + "; " + _abstract

    return summary


if __name__ == "__main__":
    main()
