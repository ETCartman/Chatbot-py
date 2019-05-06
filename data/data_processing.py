import pandas as pd
import os


def processing_movie_lines(data_path, columns):
    with open(data_path, encoding="iso-8859-1") as f:
        lines = f.readlines()
    lines = [i.split(" +++$+++ ") for i in lines]
    lines = pd.DataFrame(lines, columns=columns)
    return lines



if __name__ == '__main__':
    data_dir = ''
    lines_path = os.path.join(data_dir, 'movie_lines.txt')
    lines_cols = ["lineID", "characterID", "movieID", "character", "text"]
    lines = processing_movie_lines(lines_path, lines_cols)
    print(lines.head())