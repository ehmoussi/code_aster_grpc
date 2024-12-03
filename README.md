# Example of using grpc to call Code_Aster functions
## Prerequisites
- Code_Aster >= 16.0
- Python
  * grpcio
- Go (optional) only necessery to use the go client obviously
  * grpc

## How to (server)

The server needs to be run with python to be able to call directly
Code_Aster functions.

- Source the environment to use the prerequisites of Code_Aster 

```source .../share/aster/profile.sh```
Replace the `...` with the Code_Aster installation path

- Run the server

```python astergrpc_server/server.py```


## How to (client)

If you want to use it in different machine, you should update the host in
the client files to replace localhost with the address of the machine running the server.

- Copy `zzzz503a.mmed` file from the tests directory `.../share/aster/tests/` where `...` is the Code_Aster installation path.
- Run the client (python)
  
  ```python example.py```

- Run the client (go)
  
  ```go run main.go```

