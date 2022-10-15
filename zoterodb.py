"""
    
"""

import os
import sqlite3
import itertools
import logging


class ZoteroDB:
    """ """

    def __init__(self, data_dir):
        """ """
        self.db_dir = data_dir

        # Load on demand
        self._connection = None
        self._collections = None
        self._items = None

        # Connect to DB
        self._connect_db()

    def _connect_db(self):
        db = os.path.join(self.db_dir, "zotero.sqlite")
        if not os.path.exists(db):
            raise OSError("No database found at: {}".format(self.db_dir))

        # Connect
        self._connection = sqlite3.connect(db)
        self._connection.row_factory = sqlite3.Row
        logging.info("Connected to db")

    def _load_collections(self):
        conn = self.connection

        q = """
            SELECT
            collectionId, collectionName, parentCollectionId
            FROM collections c
        """

        collections = {}
        for c in conn.execute(q):
            collections[c["collectionID"]] = {
                "name": c["collectionName"],
                "parentID": c["parentCollectionId"],
            }

        return collections

    def _load_items(self):
        conn = self.connection

        reqItemTypes = [
            "book",
            "bookSection",
            "conferencePaper",
            "document",
            "journalArticle",
            "letter",
            "magazineArticle",
            "manuscript",
            "preprint",
            "report",
            "thesis",
            # 'attachment', 'note'
        ]
        q = """
        SELECT itemTypeID, typeName
        FROM itemTypes
        WHERE typeName IN ({})
        """.format(
            ",".join(["?"] * len(reqItemTypes))
        )

        reqItemTypeCodes = []
        itemTypeLookup = {}
        for itemType in conn.execute(q, reqItemTypes):
            itemTypeLookup[itemType["itemTypeID"]] = itemType["typeName"]
            reqItemTypeCodes.append(itemType["itemTypeID"])

        q = """
        SELECT itemID, itemTypeID, key
        FROM items
        WHERE itemTypeID IN ({}) 
        AND itemID NOT IN (SELECT itemId FROM deletedItems)
        """.format(
            ",".join(["?"] * len(reqItemTypeCodes))
        )

        items = {}
        for item in conn.execute(q, reqItemTypeCodes):
            items[item["itemID"]] = {
                "type": itemTypeLookup[item["itemTypeID"]],
                "key": item["key"],
            }

        reqItemIDs = list(items.keys())
        q = """
        SELECT id.itemID, fields.fieldName, idv.value
        FROM itemData id
        LEFT JOIN fields ON id.fieldID = fields.fieldID
        LEFT JOIN itemDataValues idv ON id.valueID = idv.valueID
        WHERE id.itemID IN ({})
        """.format(
            ",".join(["?"] * len(reqItemIDs))
        )

        for itemInfo in conn.execute(q, reqItemIDs):
            items[itemInfo["itemID"]].update(
                {itemInfo["fieldName"]: itemInfo["value"]}
            )

        q = """
        SELECT ic.itemID, ic.creatorID, c.firstName, c.lastName
        FROM itemCreators ic
        LEFT JOIN creators c ON ic.creatorID = c.creatorID
        WHERE ic.itemID IN ({})
        """.format(
            ",".join(["?"] * len(reqItemIDs))
        )
        for itemID, creatorInfo in itertools.groupby(
            conn.execute(q, reqItemIDs), key=lambda i: i["itemID"]
        ):
            _creators = []
            _creatorIDs = []
            for info in creatorInfo:
                _creatorName = "{} {}".format(
                    info["firstName"], info["lastName"]
                )
                _creators.append(_creatorName)
                _creatorIDs.append(info["creatorID"])
            items[itemID].update(
                {"creators": _creators, "creatorIDs": _creatorIDs}
            )

        return items

    def get_library(self):
        """ """
        library = {}

        conn = self.connection
        collections = self.collections
        items = self.items

        return items

    @property
    def connection(self):
        if self._connection is None:
            # attempt to connect
            self._connect_db()

        return self._connection

    @property
    def collections(self):
        if self._collections is None:
            self._collections = self._load_collections()

        return self._collections

    @property
    def items(self):
        if self._items is None:
            self._items = self._load_items()

        return self._items
