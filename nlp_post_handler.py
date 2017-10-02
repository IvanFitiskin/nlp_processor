import os
import sys

parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentdir)

from insta_post_processor.post_handler import PostHandler

from bag_creator import BagCreator
from text_preparer import TextPreparer

class NLPPostHandler(PostHandler):
    def __init__(self, text_preparer, bag_creators):
        self.text_preparer = text_preparer
        self.bag_creators = bag_creators

    def process(self, data):
        words = self.text_preparer.text_conversion(data[1])
        bags = list()
        for category in data[2]:
            creator = self.bag_creators.get(category, None)
            if creator:
                bag = creator.bag_create(words)
                bags.append(bag)
        return data[0], bags
