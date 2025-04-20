#!/bin/bash
cd ./post-comment-service
poetry run python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/postservice.proto
poetry run python -m grpc_tools.protoc -I../proto --python_out=../api-gateway --grpc_python_out=../api-gateway ../proto/postservice.proto
