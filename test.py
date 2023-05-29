# -*- coding: utf-8 -*-
import grpc
import proto.model_service_pb2
import proto.model_service_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = proto.model_service_pb2_grpc.ModelStub(channel)
    response = stub.GetGrades(proto.model_service_pb2.GradesRequest(repLink="https://github.com/your_rep_here"))
    print(response)
