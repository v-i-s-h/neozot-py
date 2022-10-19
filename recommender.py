# Recommendation engine

import logging

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

        items_embedding = self.encoder.fit_transform(items_summary.values())
        feed_embedding = self.encoder.transform(feed_summary.values())

        feed_similarity = similarity(items_embedding, feed_embedding)

        # Get top K pairs
        # Ref: https://stackoverflow.com/a/57105712
        top_K = np.c_[
            np.unravel_index(
                np.argpartition(feed_similarity.ravel(), -K)[-K:],
                feed_similarity.shape,
            )
        ]

        # Index to id mapping for library
        ids_library = list(items_summary.keys())
        # For feed, the key itself can be index, but just creating the map
        ids_feed = list(feed_summary.keys())

        recommendations = []
        for i, j in top_K:
            item_id = ids_library[i]
            feed_id = ids_feed[j]

            # print(library[item_id])
            # print(feed[feed_id])
            # print("Score: ", feed_similarity[i, j], i, j)
            # print("----")
            _item = feed[feed_id]
            _item.update({"score": feed_similarity[i, j]})
            _item.update({"related": library[item_id]})
            recommendations.append(_item)

        # sort according to score
        recommendations = sorted(
            recommendations, key=lambda x: x["score"], reverse=True
        )

        return recommendations

        # ## Alternative scoring
        # mean_scores = feed_similarity.mean(axis=0)
        # top_K = np.argpartition(mean_scores, -K)[-K:]

        # for idx in top_K:
        #     feed_id = ids_feed[idx]
        #     feed_item = feed[feed_id]
        #     print(feed_item["title"])
        #     print("\t" + feed_item["abstractNote"])
        #     print("Score = ", mean_scores[idx])

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
