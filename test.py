"""
    Neozot
"""

from zoterodb import ZoteroDB

def main():
    datadir = "data/"

    zotdb = ZoteroDB(datadir)


    library = zotdb.get_library()

    for i, (id, info) in enumerate(library.items()):
        buffer = "{:4d}\n".format(i)
        buffer += "        id              : {:4d}\n".format(id)
        for k, v in info.items():
            buffer += "        {:16s}: {}\n".format(k, v)
        print(buffer)


if __name__=="__main__":
    main()
