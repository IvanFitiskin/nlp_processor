import csv
import os
import sys

parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentdir)

from insta_post_processor.configurator.configurator import ModuleConfigurator

from bag_creator import BagCreator
from dictionary import Dictionary
from nlp_post_handler import NLPPostHandler
from text_preparer import TextPreparer

import weight_schemes as ws

class NLPPostConfigurator(ModuleConfigurator):
    def __init__(self, id):
        super(NLPPostConfigurator, self).__init__()


    def add_fields(self, configparser):
        configparser.add_section('NLP')
        configparser.set('NLP', 'dictionary_dir', '/usr/local/insta_preference_analyzer/nlp')
        configparser.set('NLP', 'meta_file', '/usr/local/insta_preference_analyzer/nlp/meta.ini')
        configparser.set('NLP', 'hashtags', 'True')
        configparser.set('NLP', 'links', 'False')
        configparser.set('NLP', 'emoji', 'False')
        # FW, JJ, JJR, JJS, MD, NN, NNS, NNP, NNPS,
        # RB, RBR, RBS, VB, VBD, VBG, VBN, VBP
        configparser.set('NLP', 'pos_eng', 'NN,VB')
        # NOUN, ADJF, ADJS, COMP, VERB, INFN, PRTF
        # PRTS, GRND, NUMR, ADVB, NPRO, PRED, PREP
        # CONJ, PRCL, INTJ
        configparser.set('NLP', 'pos_rus', 'NOUN,VERB,LATN')


    def init_module(self, configparser):
        # initialize text preparer
        hashtags = bool(configparser.get('NLP', 'hashtags'))
        links    = bool(configparser.get('NLP', 'links'))
        emoji    = bool(configparser.get('NLP', 'emoji'))
        pos_eng  = configparser.get('NLP', 'pos_eng')
        pos_rus  = configparser.get('NLP', 'pos_rus')
        text_preparer = TextPreparer(hashtags, links, emoji, pos_eng, pos_rus)

        dictionary_dir = configparser.get('NLP', 'dictionary_dir')
        # initialize bag creators
        bag_creators = dict()
        meta_file = configparser.get('NLP', 'meta_file')
        meta_reader = csv.reader(open(meta_file, 'r'), delimiter=';')
        next(meta_reader)
        for line in meta_reader:
            filename          = os.path.join(dictionary_dir, line[0])
            category          = line[1]
            schema            = ws.SCHEMES[line[2]]
            count             = int(line[3])
            dictionary_reader = csv.reader(open(filename, 'r'), delimiter=';')
            next(dictionary_reader)
            words_count = list()
            for index, word_data in enumerate(dictionary_reader):
                if index >= count:
                    break
                words_count.append((word_data[0], (int(word_data[1]), int(word_data[2]))))
            dictionary  = Dictionary(words_count)
            bag_creator = BagCreator(dictionary, category, schema)
            bag_creators[category] = bag_creator
        return NLPPostHandler(text_preparer, bag_creators)
