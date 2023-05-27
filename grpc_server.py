import subprocess
import os

import config

import grpc
import proto.model_service_pb2 as msClasses
import proto.model_service_pb2_grpc as msGrpc

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optimizer
import numpy as np

    
regression_model = tf.saved_model.load(config.SAVED_MODEL_PATH)

class ModelService(msGrpc.ModelServicer):
    def GetGrades(self, request, context):
        link = request.repLink
        # The sctipt returns path to diffs folder
        output = subprocess.run(['bash', './analyze.sh', link], capture_output=True, text=True)
        # Need a substring because the outupt have a \n at line end
        work_dir = output.stdout[:-1] 
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

        for author in diffs_by_author:
            testing_data = split_by_chunks(diffs_by_author[author])
            predictions = regression_model(testing_data)
            print(f"{author}:\n\tPrediction salary =  ~", np.mean(predictions) * SCALE_RATIO)
            del predictions
            del diffs_by_author[author]

        return super().GetGrades(request, context)


def split_by_chunks(data: str):
    X = []
    for text in data:
        chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        if chunks:
            X += chunks
    return X


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msGrpc.add_ModelServicer_to_server(ModelService, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

