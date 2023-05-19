import sys

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optimizer

import matplotlib.pyplot as plt
import numpy as np

tf.get_logger().setLevel('ERROR')

# PREPROCESSOR = 'https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/3'
PREPROCESSOR = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
# MODEL = 'https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/4'
MODEL = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/2'
MODEL_NAME = MODEL.replace('https://tfhub.dev/tensorflow/', '')

SAVED_MODEL_PATH = './saved_git_model/{}_bert'.format(MODEL_NAME.replace('/', '_'))

SCALE_RATIO = 2.5 * 100000

CHUNK_SIZE = 100 * 3

diffs_file = sys.argv[1]

testing_data = ''
try:
    with open(diffs_file, encoding='utf-8') as f:
        testing_data = "".join(f.readlines())
except FileNotFoundError as e:
    print('no diffs found!:', e)
except UnicodeDecodeError as e:
    print('UnicodeDecodeError: ', e)

def string_by_chunks(data):
    X = []
    for text in data:
        chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        if chunks:
            X += chunks
    return X

testing_data = string_by_chunks(testing_data)

regression_model = tf.saved_model.load(SAVED_MODEL_PATH)

predictions = regression_model.predict(testing_data)

print("Prediction salary: ", np.mean(predictions))