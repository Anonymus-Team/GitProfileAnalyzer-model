MODEL = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/2'
MODEL_NAME = MODEL.replace('https://tfhub.dev/tensorflow/', '')
SAVED_MODEL_PATH = './saved_git_model/{}_bert'.format(MODEL_NAME.replace('/', '_'))