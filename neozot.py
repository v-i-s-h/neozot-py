"""
    Neozot
"""

from zoterodb import ZoteroDB


def main():
    datadir = "data/"

    zotdb = ZoteroDB(datadir)


    library = zotdb.get_library()
    
    display_library(library)

    # Build a summary of each item, only if it has abstract
    summary = build_summary(library)
    print("Created summary for {}/{} documents.".format(
        len(summary), len(library)))

    #


def display_library(library):
    for i, (id, info) in enumerate(library.items()):
        buffer = "{:4d}\n".format(i)
        buffer += "        id              : {:4d}\n".format(id)
        for k, v in info.items():
            buffer += "        {:16s}: {}\n".format(k, v)
        print(buffer)


def build_summary(library):
    summary = {}
    for id, info in library.items():
        _title = info.get('title', None)
        _abstract = info.get('abstractNote', None)
        if _title and _abstract:
            summary[id] = _title + ' ' + _abstract

    return summary

if __name__=="__main__":
    main()
