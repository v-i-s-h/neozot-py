# Recommendation engine

import logging
from copy import deepcopy

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel as similarity


def build_summary(library):
    summary = {}
    for id, info in library.items():
        _title = info.get("title", None)
        _abstract = info.get("abstractNote", None)
        if _title and _abstract:
            summary[id] = _title + "; " + _abstract

    return summary


class Recommender:
    def __init__(self):
        # Create feature builder
        self.encoder = TfidfVectorizer(
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

    def get_recommendations(self, library, feed, K=10):
        # Build a summary of each item, only if it has abstract
        items_summary = build_summary(library)
        logging.info(
            "Created summary for {}/{} documents.".format(
                len(items_summary), len(library)
            )
        )

        feed_summary = build_summary(feed)
        logging.info(
            "Created summary for {}/{} feed items.".format(
                len(feed_summary), len(feed)
            )
        )

        # Creating list of mappings
        items_summary_ids = []
        items_summary_values = []
        for id, val in items_summary.items():
            items_summary_ids.append(id)
            items_summary_values.append(val)
        feed_summary_ids = []
        feed_summary_values = []
        for id, val in feed_summary.items():
            feed_summary_ids.append(id)
            feed_summary_values.append(val)

        items_embedding = self.encoder.fit_transform(items_summary_values)
        feed_embedding = self.encoder.transform(feed_summary_values)

        feed_similarity = similarity(items_embedding, feed_embedding)
        # Feed similarity matrix is a matrix of dimension
        #       items x feeds
        # We find top K entries in the matrix to find top K pairs

        # Get top K pairs
        # Ref: https://stackoverflow.com/a/57105712
        top_K = np.c_[
            np.unravel_index(
                np.argpartition(feed_similarity.ravel(), -K)[-K:],
                feed_similarity.shape,
            )
        ]

        recommendations = []
        for i, j in top_K:
            item_id = items_summary_ids[i]
            feed_id = feed_summary_ids[j]

            # Deep copy is required, otherwise we will be modifying the original
            # entry itself later
            _item = deepcopy(feed[feed_id])
            _item.update({"score": feed_similarity[i, j]})
            _item.update({"related": deepcopy(library[item_id])})

            recommendations.append(_item)

        # sort according to score
        recommendations = sorted(
            recommendations, key=lambda x: x["score"], reverse=True
        )

        ## Alternative scoring
        scores = feed_similarity.sum(axis=0)
        top_K = np.argpartition(scores, -K)[-K:]

        recommendations = []
        for idx in top_K:
            feed_id = feed_summary_ids[idx]
            
            _item = deepcopy(feed[feed_id])
            _item.update({"score": scores[idx]})
            _item.update({"related": ""})

            recommendations.append(_item)

        # sort according to score
        recommendations = sorted(
            recommendations, key=lambda x: x["score"], reverse=True
        )

        # # Print feed similarity
        # n_feed = len(feed_summary)
        # n_items = len(items_summary)
        # for i, (id, info) in enumerate(library.items()):
        #     print("{:3d}. {}".format(i + 1, info["title"]))
        # for i, (id, info) in enumerate(feed.items()):
        #     print("{:3d}.    ".format(i + 1), end="")
        #     for j in range(n_items):
        #         print("{:.4f}    ".format(feed_similarity[j, i]), end="")
        #     print(
        #         "[{:.4f}] {} ".format(mean_scores[i], "*" if i in top_K else " "),
        #         end="",
        #     )
        #     print("{:120s}  {:30s}".format(info["title"], info["link"]))

        return recommendations