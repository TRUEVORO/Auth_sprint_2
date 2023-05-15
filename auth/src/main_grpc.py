from concurrent import futures

import grpc

from core import settings
from core.grpc.user_pb2_grpc import add_DetailerServicer_to_server
from services.grpc import UserFetcher

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor())

    add_DetailerServicer_to_server(UserFetcher(), server)

    server.add_insecure_port(f'[::]:{settings.grpc_port}')
    server.start()
    server.wait_for_termination()
