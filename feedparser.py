"""
    Parse RSS feed from arxiv
"""

import xml.etree.ElementTree as ET


if __name__=="__main__":
    feedfile = "./feeds/cs.LG.xml"

    feedtree = ET.parse(feedfile) # Can also parse from fromstring

    root = feedtree.getroot()

    # print(root.tag, root.attrib)

    # for child in root:
    #     print(child.tag, child.attrib)

    # <rdf:RDF 
    #     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    #     xmlns="http://purl.org/rss/1.0/" 
    #     xmlns:content="http://purl.org/rss/1.0/modules/content/" 
    #     xmlns:taxo="http://purl.org/rss/1.0/modules/taxonomy/" 
    #     xmlns:dc="http://purl.org/dc/elements/1.1/" 
    #     xmlns:syn="http://purl.org/rss/1.0/modules/syndication/" 
    #     xmlns:admin="http://webns.net/mvcb/"
    # >

    ns = {
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'content': "http://purl.org/rss/1.0/modules/content/",
        'taxo': "http://purl.org/rss/1.0/modules/taxonomy/",
        'dc': "http://purl.org/dc/elements/1.1/",
        'syn': "http://purl.org/rss/1.0/modules/syndication/",
        'admin': "http://webns.net/mvcb/",
        '': "http://purl.org/rss/1.0/"
    }

    # Get all items in this feed
    for i, item in enumerate(root.findall('item', ns)):
        # print(">>", item.tag, item.attrib)
        # for child in item:
        #     print("    ", child.tag, child.text)
        title = item.find('title', ns).text
        link = item.find('link', ns).text
        desc = item.find('description', ns).text.replace("\n", " ")
        creators = item.find('dc:creator', ns).text

        print("{:3d}. {}".format(i, title))
        print("        Link        : {}".format(link))
        print("        Description : {}".format(desc))
        print("        Creators    : {}".format(creators))