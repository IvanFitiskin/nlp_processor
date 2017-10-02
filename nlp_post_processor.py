import os
import sys

parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentdir)

from insta_post_processor.post_processor import AbstractPostProcessor
from insta_post_processor.post_processor import start_processor

from nlp_post_configurator import NLPPostConfigurator
from nlp_json_processor import NLPJsonProcessor

import time

class NLPPostProcessor(AbstractPostProcessor):
    def __init__(self, config_file, suffix=''):
        super(NLPPostProcessor, self).__init__(config_file, suffix)
        self.__init_params()

    def __init_params(self):
        self.post_configurator = NLPPostConfigurator(self.id)
        self.json_processor = NLPJsonProcessor()


if __name__ == '__main__':
    start_processor(NLPPostProcessor)
