import sys
import os
import argparse 

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optimizer
import numpy as np

tf.get_logger().setLevel('ERROR')


DESCRIPTION = "Classification developers by their commits "

parser = argparse.ArgumentParser(
                    description=DESCRIPTION)
parser.add_argument('diffs_dirs', metavar='DIR')

args = parser.parse_args()
work_dir = args.diffs_dirs


PREPROCESSOR = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
MODEL = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/2'
MODEL_NAME = MODEL.replace('https://tfhub.dev/tensorflow/', '')

SAVED_MODEL_PATH = './saved_git_model/{}_bert'.format(MODEL_NAME.replace('/', '_'))

SCALE_RATIO = 2.5 * 100000

CHUNK_SIZE = 100 * 3

diffs_by_author = {}

try:
    auhors_dirs = os.listdir(work_dir)

    # build path to found directories
    auhors_dirs = [os.path.join(work_dir, p) for p in auhors_dirs]
    for d in auhors_dirs:
        with open(os.path.join(d, 'author.email')) as e:
            email = e.readline()
        with open(os.path.join(d, 'history')) as h:
            history = ''.join(h.readlines())    # read all file
        diffs_by_author[email] = history
except FileNotFoundError as e:
    print('no diffs found!:', e)
except UnicodeDecodeError as e:
    print('UnicodeDecodeError: ', e)

def split_by_chunks(data: str):
    X = []
    for text in data:
        chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        if chunks:
            X += chunks
    return X

regression_model = tf.saved_model.load(SAVED_MODEL_PATH)
print('loading model: done')

for author in diffs_by_author:
    testing_data = split_by_chunks(diffs_by_author[author])
    predictions = regression_model(testing_data)
    print(f"{author}:\n\tPrediction salary =  ~", np.mean(predictions) * SCALE_RATIO)
    del predictions
    del diffs_by_author[author]