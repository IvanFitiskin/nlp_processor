from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


import nltk
import re
import string
import pymorphy2


class TextPreparer:

    EMOJI_EMOTICONS_SYMBOLS = u"\U0001F600-\U0001F64F"
    EMOJI_PICTOGRAPHS_SYMBOLS = u"\U0001F300-\U0001F5FF"
    EMOJI_TRANSPORT_MAP_SYMBOLS = u"\U0001F680-\U0001F6FF"
    EMOJI_FLAG_IOS = u"\U0001F1E0-\U0001F1FF"
    EMOJI_OTHER = u"\U0001F913-\U0001F919"
    EMOJI_PATTERN = re.compile("[" + EMOJI_EMOTICONS_SYMBOLS + EMOJI_PICTOGRAPHS_SYMBOLS + EMOJI_TRANSPORT_MAP_SYMBOLS + EMOJI_FLAG_IOS + EMOJI_OTHER + "]", flags=re.UNICODE)

    REGEX_LINK = re.compile(r'@\w+')

    REGEX_HASH_TAGS = re.compile(r'#\w+')

    PUNCTUATION_SYMBOLS = '~!@#$%^&*():;-_+=\t,\.\\/[]{}"\'|`?'
    REGEX_PUNCTUATION = re.compile('[%s0-9]+' % re.escape(string.punctuation + PUNCTUATION_SYMBOLS))

    REGEX_TOKENIZE_ENG = re.compile('[a-z]+')

    REGEX_TOKENIZE_RU = re.compile('[а-я,ё]+')

    STOP_WORDS_ENG = set(stopwords.words('english'))
    STOP_WORDS_RU = set(stopwords.words('russian'))

    LEMMATIZER = WordNetLemmatizer()

    MORPH = pymorphy2.MorphAnalyzer()

    def __init__(self, hash_tags, links, emoji, pos_tags_eng, pos_tags_ru):
        self.hash_tags = hash_tags
        self.links = links
        self.emoji = emoji
        self.pos_tags_eng = pos_tags_eng.split(',')
        self.pos_tags_ru = pos_tags_ru.split(',')

    def text_conversion(self, text):
        text = text.lower()

        if (self.hash_tags):
            text = self.REGEX_HASH_TAGS.sub(' ', text).strip()

        if (self.links):
            text = self.REGEX_LINK.sub(' ', text).strip()

        if (self.emoji):
            text = self.EMOJI_PATTERN.sub(r' ', text).strip()

        text = self.REGEX_PUNCTUATION.sub(' ', text).strip()

        words_eng = self.REGEX_TOKENIZE_ENG.findall(text)
        words_eng = self.cleaning_unused_pos(self.filtered_sentence(words_eng, self.STOP_WORDS_ENG))
        words_eng = self.lemmatizing_text(words_eng)

        words_ru = self.REGEX_TOKENIZE_RU.findall(text)
        words_ru = self.cleaning_unused_pos_ru(self.filtered_sentence(words_ru, self.STOP_WORDS_RU))
        words_ru = self.lemmatizing_text_ru(words_ru)

        return list(words_eng + words_ru)

    def filtered_sentence(self, words, language):
        return [w for w in words if len(w) > 2 and not w in language]

    def cleaning_unused_pos(self, words):
        words_and_tags = nltk.pos_tag(words)
        result = list()

        for word, tag in words_and_tags:
            if tag in self.pos_tags_eng:
                result.append(word)
        return result

    def lemmatizing_text(self, words):
        result = list()

        for word in words:
            result.append(self.LEMMATIZER.lemmatize(word))

        return result

    def cleaning_unused_pos_ru(self, words):
        result = list()

        for word in words:
            if self.MORPH.parse(word)[0].tag.POS in self.pos_tags_ru:
                result.append(word)

        return result

    def lemmatizing_text_ru(self, words):
        result = list()

        for word in words:
            result.append(self.MORPH.parse(word)[0].normal_form)

        return result
