"""
    Parse RSS feed from arxiv
"""

import xml.etree.ElementTree as ET
import re


class ArxivFeedProvider:
    def __init__(self, domains=None) -> None:
        self.domains = domains

    def get_feed(self):
        feedfile = "./feeds/cs.LG.xml"
        feedtree = ET.parse(feedfile) # Can also parse from fromstring
        root = feedtree.getroot()

        ns = {
            'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            'content': "http://purl.org/rss/1.0/modules/content/",
            'taxo': "http://purl.org/rss/1.0/modules/taxonomy/",
            'dc': "http://purl.org/dc/elements/1.1/",
            'syn': "http://purl.org/rss/1.0/modules/syndication/",
            'admin': "http://webns.net/mvcb/",
            '': "http://purl.org/rss/1.0/"
        }

        # print(root.tag, root.attrib)
        # for child in root:
        #     print(child.tag, child.attrib)

        # Get all items in this feed
        feed_items = {}
        for i, item in enumerate(root.findall('item', ns)):
            # print(">>", item.tag, item.attrib)
            # for child in item:
            #     print("    ", child.tag, child.text)
            title = item.find('title', ns).text
            link = item.find('link', ns).text
            desc = item.find('description', ns).text.replace("\n", " ")
            creators = item.find('dc:creator', ns).text

            # Clean up
            title = re.sub("\.\s\([^)]+\)", "", title)
            desc = desc[3:-6]
            creators = re.sub("<.+?>", "", creators).split(', ')

            # print("{:3d}. {}".format(i, title))
            # print("        Link        : {}".format(link))
            # print("        Description : {}".format(desc))
            # print("        Creators    : {}".format(creators))

            feed_items[i] = {
                'title': title,
                'abstractNote': desc,
                'creators': creators,
                'link': link
            }

        return feed_items
