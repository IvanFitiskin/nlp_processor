import weight_schemes as ws
import post_vector

class BagCreator:
    def __init__(self, dictionary, category, schema=ws.boolean):
        self.dictionary = dictionary
        self.category = category
        self.schema = schema

    def bag_create(self, words):
        vector = list()
        word_values = dict()

        for word in words:
            word_index = self.dictionary.get_index(word)
            if not word_index:
                continue
            count = word_values.get(word_index, 0)
            word_values[word_index] = count + 1

        for word_index, value in word_values.items():
            posts_count, total = self.dictionary.get_posts_values(word_index)
            weight = self.schema(value, len(words), posts_count,total)
            vector.append(post_vector.WordInfo(word_index, weight))
        return post_vector.PostVector(self.category, vector)
