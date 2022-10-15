"""
    Parse RSS feed from arxiv
"""

import os
from datetime import datetime
import requests
import json
import xml.etree.ElementTree as ET
import re
import logging


class ArxivFeedProvider:
    def __init__(self, domains=None, feeddir="feeds/") -> None:
        default_domains = ["cs.AI", "cs.CV", "cs.LG"]
        self.baseurl = "http://arxiv.org/rss/"
        if domains is not None:
            self.domains = domains
        else:
            self.domains = default_domains
        self.feeddir = feeddir

    def _download_feeds(self, force_refresh=False):
        """
        Download recent feeds
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        # Make directory for today
        outdir = os.path.join(self.feeddir, timestamp)
        os.makedirs(outdir, exist_ok=True)

        feedfiles = []
        for domain in self.domains:
            feedurl = self.baseurl + domain
            outfile = os.path.join(outdir, domain + ".xml")
            # If file exists, do not download
            if os.path.exists(outfile) and not force_refresh:
                logging.info("Feed cache found {}".format(outfile))
                feedfiles.append(outfile)
            else:
                logging.info("Downloading feeds for domain {}".format(domain))
                status_ok = self._download_feed(feedurl, outfile)
                if status_ok:
                    feedfiles.append(outfile)
                else:
                    logging.error(
                        "ERROR downloading {}. Status: {}".format(
                            domain, status_ok
                        )
                    )

        # return all feed files
        return feedfiles

    def _download_feed(self, url, outfile):
        """
        Download feed and write to given file
        """
        status = False

        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            # Write out the feed
            with open(outfile, "wb") as f:
                f.write(r.content)
            with open(outfile + ".header.json", "w") as f:
                json.dump(dict(r.headers), f)
            status = True

        return status

    def _parse_feed(self, feedfile):
        feedtree = ET.parse(feedfile)  # Can also parse from fromstring
        root = feedtree.getroot()

        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "content": "http://purl.org/rss/1.0/modules/content/",
            "taxo": "http://purl.org/rss/1.0/modules/taxonomy/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "syn": "http://purl.org/rss/1.0/modules/syndication/",
            "admin": "http://webns.net/mvcb/",
            "": "http://purl.org/rss/1.0/",
        }

        # print(root.tag, root.attrib)
        # for child in root:
        #     print(child.tag, child.attrib)

        # Get all items in this feed
        feed_items = {}
        for i, item in enumerate(root.findall("item", ns)):
            # print(">>", item.tag, item.attrib)
            # for child in item:
            #     print("    ", child.tag, child.text)
            title = item.find("title", ns).text
            link = item.find("link", ns).text
            desc = item.find("description", ns).text.replace("\n", " ")
            creators = item.find("dc:creator", ns).text

            # Clean up
            title = re.sub("\.\s\([^)]+\)", "", title)
            desc = desc[3:-6]
            creators = re.sub("<.+?>", "", creators).split(", ")
            id = link.split("/")[-1]  # archiv ID

            # print("{:3d}. {}".format(i, title))
            # print("        ID          : {}".format(id))
            # print("        Link        : {}".format(link))
            # print("        Description : {}".format(desc))
            # print("        Creators    : {}".format(creators))

            feed_items[id] = {
                "title": title,
                "abstractNote": desc,
                "creators": creators,
                "link": link,
            }

        return feed_items

    def get_feed_summary(self, force_refresh=False):

        feed_files = self._download_feeds(force_refresh)
        feeditems = {}

        for feedfile in feed_files:
            # Each feed dictionary is merged to the final feed dictionary
            # using the arxiv id as key. This way, duplicate entries are
            # purged automatically
            feeddict = self._parse_feed(feedfile)
            feeditems.update(feeddict)

        return feeditems
