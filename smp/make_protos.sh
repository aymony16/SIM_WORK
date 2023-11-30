#!/bin/bash

# Install the necessary tools
pip install grpcio-tools

# Navigate to the directory containing your .proto file
# cd /path/to/your/proto/file

# Generate the Python and gRPC code
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. smp.proto