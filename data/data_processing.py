import pandas as pd
import os


def processing_movie_lines(data_path, data_cols):
    with open(data_path, encoding="iso-8859-1") as f:
        lines = f.readlines()
    lines = [i.split(" +++$+++ ") for i in lines]
    print(lines[0])


if __name__ == '__main__':
    data_dir = ''
    data_path = os.path.join(data_dir, 'movie_lines.txt')
    processing_movie_lines(data_path, '')