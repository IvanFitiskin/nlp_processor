import os
import sys

parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentdir)

from insta_post_processor.json_processor import JSONProcessor

import json

class NLPJsonProcessor(JSONProcessor):
    def parse_line(self, line):
        parsed_json = json.loads(line)
        return parsed_json['post_id'], parsed_json['text'], parsed_json['categories'].split(',')

    def pack_data(self, data):
        json_message = {
            "post_id" : data[0],
            "bags"    : list()
        }

        for bag in data[1]:
            weights = ['{0}:{1}'.format(info.index, info.value) for info in bag.values if info.value != 0.0 ]
            bag_message = {
                "category"    : bag.categories,
                "post_vector" : ','.join(weights)
            }
            json_message["bags"].append(bag_message)

        return json.dumps(json_message)
