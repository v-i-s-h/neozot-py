"""
    Recommender based on Semantic Scholar's SPECTER Embeddings

    Status: Experimental
"""


from .zoterodb import ZoteroDB

import os
import pickle as pkl
import requests


URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16


def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def embed(papers):
    embeddings_by_paper_id = {}

    for chunk in chunks(papers):
        response = requests.post(URL, json=chunk)

        if response.status_code != 200:
            raise RuntimeError("Error occured")

        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]

    return embeddings_by_paper_id


if __name__ == "__main__":
    # Load zotero library
    DATADIR = "./data/"

    zotdb = ZoteroDB(DATADIR)
    zotlib = zotdb.get_library()

    library = []
    for id, info in zotlib.items():
        _title = info.get("title", None)
        _abstract = info.get("abstractNote", None)
        if _title and _abstract:
            this_item = {"paper_id": id, "title": _title, "abstract": _abstract}
            library.append(this_item)

    print("Creating embeddings for {} items".format(len(library)))
    embeddings = embed(library)

    for item in library:
        id = item["paper_id"]
        emb = embeddings[id]
        item["emb"] = emb

    emb_file = os.path.join(DATADIR, "embeddings.pkl")
    with open(emb_file, "wb") as f:
        pkl.dump(library, f)
