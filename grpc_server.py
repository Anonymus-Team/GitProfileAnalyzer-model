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


class ModelService(msGrpc.ModelServicer):
    def GetGrades(self, request, context):
        link = request.repLink
        return super().GetGrades(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msGrpc.add_ModelServicer_to_server(ModelService, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    regression_model = tf.saved_model.load(config.SAVED_MODEL_PATH)
    print('loading model: done')
    serve()

