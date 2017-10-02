class Dictionary:
    def __init__(self):
        self.total            = 0
        self.word_index       = dict()
        self.count_list       = list()
        self.posts_count_list = list()

    def __init__(self, word_count):
        word_index = 0
        self.total = 0
        self.word_index       = dict()
        self.count_list       = list()
        self.posts_count_list = list()
        for word, counts in word_count:
            if not (word in self.word_index):
                self.count_list.append(counts[0])
                self.posts_count_list.append(counts[1])
                self.word_index[word] = word_index
                self.total += counts[1]
                word_index += 1

    def inc_count(self, word, count):
        index = self.word_index.get(word, len(self.count_list))
        if index == len(self.count_list):
            self.word_index[word] = index
            self.count_list.append(count)
        else:
            self.count_list[index] += count

    def get_index(self, word):
        return self.word_index.get(word, None)

    def get_count(self, word):
        index = self.get_index(word)
        if index:
            return self.count_list[index]
        else:
            return 0

    def get_posts_values(self, word):
        index = self.get_index(word)
        posts_count = 0
        if index:
            posts_count =  self.posts_count_list[index]
        return posts_count, self.total
