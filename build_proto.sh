python -m grpc_tools.protoc -Iinterfaces/python=proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/code_aster.proto

protoc --go_out=interfaces/go --go_opt=paths=source_relative --go-grpc_out=interfaces/go --go-grpc_opt=paths=source_relative ./proto/code_aster.proto
