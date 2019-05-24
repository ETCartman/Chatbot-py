# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 下午6:44
# @Author  : Hj Liu
# @FileName: data_utils.py
import pandas as pd
import os
from tqdm import tqdm


class DataFormatter(object):
    """
    This class is used for formatting raw data.
    """
    def __init__(self, data_dir, movie_lines_file='movie_lines.txt',
                 movie_conversations_file='movie_conversations.txt',
                 save_file='formatted_movie_lines.txt'):
        """
        class init
        Args:
            data_dir: data dir
            movie_lines_file: movie lines file name
            movie_conversations_file: movie conversations filename.
            save_file: Filename to save formatted data.
        """
        self.data_dir = data_dir

        self.movie_lines_file = movie_lines_file
        self.movie_lines_cols = ["lineID", "characterID", "movieID", "character", "text"]

        self.movie_conversations_file = movie_conversations_file
        self.movie_conversations_cols = ["character1ID", "character2ID", "movieID", "utteranceIDs"]

        self.save_file = save_file
        self.save_file_cols = ["query", 'answer']

    def processing_movie_lines(self):
        """

        Returns:

        """
        data_path = os.path.join(self.data_dir, self.movie_lines_file)
        with open(data_path, encoding="iso-8859-1") as f:
            lines = f.readlines()
        lines = [i.split(" +++$+++ ") for i in lines]
        lines = pd.DataFrame(lines, columns=self.movie_lines_cols)
        lines_dict = {}
        print("[+] Processing movie lines...")
        for line_id, text in tqdm(zip(lines['lineID'], lines['text'])):
            lines_dict[line_id] = text
        return lines, lines_dict

    def processing_movie_conversations(self, lines_dict):
        """

        Args:
            lines_dict:

        Returns:

        """
        data_path = os.path.join(self.data_dir, self.movie_conversations_file)
        with open(data_path, encoding="iso-8859-1") as f:
            conversations = f.readlines()
        conversations = [i.split(" +++$+++ ") for i in conversations]
        conversations = pd.DataFrame(conversations, columns=self.movie_conversations_cols)
        conversations_line_id = [eval(i) for i in conversations['utteranceIDs']]
        print("[+] Processing movie conversations...")
        conversations_lines = []
        for line_ids in tqdm(conversations_line_id):
            single_text = []
            for line_id in line_ids:
                text = lines_dict[line_id].strip()
                single_text.append(text)
            conversations_lines.append(single_text)
        return conversations_lines

    def extract_sentence_pairs(self, conversations):
        """

        Args:
            conversations:

        Returns:

        """
        qa_pairs = []
        for conversation in tqdm(conversations):
            for i in range(len(conversation) - 1):
                query = conversation[i]
                answer = conversation[i + 1]
                if query and answer:
                    qa_pairs.append([query, answer])
        qa_pairs = pd.DataFrame(qa_pairs, columns=self.save_file_cols)
        return qa_pairs

    def generate_formatted_data(self):
        """

        Returns:

        """
        _, lines_dict = self.processing_movie_lines()
        conversations_lines = self.processing_movie_conversations(lines_dict)
        qa_pairs = self.extract_sentence_pairs(conversations_lines)
        return qa_pairs


class Voc(object):
    """
    This class is used for mapping words to index
    and trimming data.
    """
    def __init__(self, name):
        self.name = name  # Vocabulary's name.
        self.trimmed = False  # If data is trimmed it should be True.
        self.word_to_index = {}  # Mapping words to index.
        self.index_to_word = {0: "PAD", 1: "SOS", 2: "EOS"}  # Mapping index to word.
        self.word_to_count = {}  # Mapping words to the number of itself.
        self.num_words = 3  # The number of set of all words.

    def add_word(self, word):
        """
        Add one word to vocabulary.
        Args:
            word: English word.

        Returns:
            None

        """
        if not self.word_to_index.get(word, None):  # If "word" is in our vocabulary.
            self.word_to_index[word] = self.num_words
            self.index_to_word[self.num_words] = word
            self.word_to_count[word] += 1
            self.num_words += 1
        else:
            self.word_to_count[word] += 1

    def add_sentence(self, sentence):
        """
        This function is used for splitting one sentence to words and
        adding those word to our vocabulary.
        Args:
            sentence: English sentence

        Returns:
            None
        """
        for word in sentence.split(" "):  # "This is fabulous" -> ["This", "is", "fabulous"]
            self.add_word(word)  # add word to vocabulary.

    def sentence_padding(self, sentence, max_length):
        """
        Padding sentence if it's length less than max_length or trimming sentence
        if it's length is more than max_length.
        Args:
            sentence: Sentence to pad or trim.
            max_length: Sentence length threshold.

        Returns:
            None
        """

    def trim(self, mini_count):
        """
        Remove words below a certain count threshold
        Args:
            mini_count:

        Returns:

        """
        if self.trimmed:
            return

        keep_words = []  # Words which
        for word, count in self.word_to_count.values():
            if count >= mini_count:
                keep_words.append(word)


if __name__ == '__main__':
    data_format = DataFormatter('.')
    print(data_format.generate_formatted_data())
