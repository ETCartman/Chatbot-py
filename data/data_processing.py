import pandas as pd
import os
from tqdm import tqdm


def processing_movie_lines(data_path, columns):
    with open(data_path, encoding="iso-8859-1") as f:
        lines = f.readlines()
    lines = [i.split(" +++$+++ ") for i in lines]
    lines = pd.DataFrame(lines, columns=columns)
    lines_dict = {}
    print("[+] Processing movie lines...")
    for line_id, text in tqdm(zip(lines['lineID'], lines['text'])):
        lines_dict[line_id] = text
    return lines, lines_dict


def processing_movie_conversations(data_path, columns, lines_dict):
    with open(data_path, encoding="iso-8859-1") as f:
        conversations = f.readlines()
    conversations = [i.split(" +++$+++ ") for i in conversations]
    conversations = pd.DataFrame(conversations, columns=columns)
    conversations_lineid = [eval(i) for i in conversations['utteranceIDs']]
    print("[+] Processing movie conversations...")
    conversations_lines = []
    for line_ids in tqdm(conversations_lineid):
        single_text = []
        for line_id in line_ids:
            text = lines_dict[line_id].strip()
            single_text.append(text)
        conversations_lines.append(single_text)
    return conversations_lines


def extract_sentence_pairs(conversations):
    qa_pairs = []
    for conversation in tqdm(conversations):
        for i in range(len(conversation) - 1):
            query = conversation[i]
            answer = conversation[i+1]
            if query and answer:
                qa_pairs.append([query, answer])
    qa_pairs = pd.DataFrame(qa_pairs, columns=["query", 'answer'])
    return qa_pairs


if __name__ == '__main__':
    data_dir = ''
    lines_path = os.path.join(data_dir, 'movie_lines.txt')
    lines_cols = ["lineID", "characterID", "movieID", "character", "text"]
    lines, lines_dict = processing_movie_lines(lines_path, lines_cols)

    conversation_path = os.path.join(data_dir, 'movie_conversations.txt')
    conversations_cols = ["character1ID", "character2ID", "movieID", "utteranceIDs"]
    conversations = processing_movie_conversations(conversation_path, conversations_cols, lines_dict)
    qa_pair = extract_sentence_pairs(conversations)
    qa_pair.to_csv('formatted_movie_lines.txt', sep='\t', encoding="utf-8", index=None)