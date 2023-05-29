import subprocess
import os
import logging
from concurrent import futures

import grpc

import proto.model_service_pb2 as msClasses
import proto.model_service_pb2_grpc as msGrpc
import binary_reader
import config

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import numpy as np

tf.get_logger().setLevel('ERROR')
logging.basicConfig(level=logging.INFO)

logging.info('Loading model {config.SAVED_MODEL_PATH}')
regression_model = tf.saved_model.load(config.SAVED_MODEL_PATH)
logging.info('Model was loaded')

r_gen = np.random.default_rng()

class ModelService(msGrpc.ModelServicer):
    def GetGrades(self, request, context):
        link = request.repLink
        logging.info(f"Downloading and processing the repository: {link}")
        # The sctipt returns path to diffs folder
        output = subprocess.run(['bash', './analyze.sh', link], capture_output=True, text=True)
        # Need a substring because the outupt have a \n at line end
        work_dir = output.stdout[:-1] 
        diffs_by_author = {}

        auhors_dirs = os.listdir(work_dir)

        logging.info("Reading diffs...")
        # build path to found directories
        auhors_dirs = [os.path.join(work_dir, p) for p in auhors_dirs]
        for d in auhors_dirs:
            with open(os.path.join(d, 'author.email'), encoding='utf-8') as e:
                email = e.readline()
            
            history = binary_reader.read_file(os.path.join(d, 'history'))

            diffs_by_author[email] = history

        response = msClasses.Grades()

        for author in diffs_by_author:
            logging.info(f"Split data by chunks for {author}")
            testing_data = split_by_chunks(diffs_by_author[author])
            
            # sparse data to optimize performance
            if config.OPTIMIZE:
                max_samples = config.PREDICT_CLIP
                if max_samples > len(testing_data):
                    max_samples = len(testing_data)
                indexes = r_gen.integers(0, len(testing_data), max_samples)
                testing_data = [testing_data[i] for i in indexes]

            logging.info(f"Running model for {author}")
            predictions = regression_model(testing_data)

            salary = np.mean(predictions) * config.SCALE_RATIO 
            grade = msClasses.Grade(nickname=author, salary=float(salary))
            response.grade.append(grade)

            del predictions
        del diffs_by_author

        return response


def split_by_chunks(data: str):
    X = []
    for text in data:
        chunks = [text[i:i+config.CHUNK_SIZE] for i in range(0, len(text), config.CHUNK_SIZE)]
        if chunks:
            X += chunks
    return X


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msGrpc.add_ModelServicer_to_server(ModelService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

