"""
    Neozot
"""

from zoterodb import ZoteroDB

def main():
    datadir = "data/"

    zotdb = ZoteroDB(datadir)


    library = zotdb.get_library()

    for i, (key, info) in enumerate(library.items()):
        print(key, info)

        if i > 9: 
            break


if __name__=="__main__":
    main()
