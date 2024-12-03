# python
python -m grpc_tools.protoc `
    -Iinterfaces/python=proto `
    --python_out=. `
    --pyi_out=. `
    --grpc_python_out=. `
    ./proto/code_aster.proto

# go
.\protoc-29.0-win64\bin\protoc.exe `
    --go_out=. `
    --go_opt=Mproto/code_aster.proto=interfaces/go `
    --go-grpc_out=. `
    --go-grpc_opt=Mproto/code_aster.proto=interfaces/go `
    ./proto/code_aster.proto