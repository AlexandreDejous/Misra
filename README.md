Semestral work on misra's detection of distributed computation.

Leverages gRPC, python.

The part using gRPC was built upon gRPC python hello world example (https://grpc.io/docs/quickstart/python.html)

Misra’s algorithm (named after Jayadev Misra) allows for detection of termination of computation
in an arbitrary network. This problem is qualified in the original paper as of “considerable
importance”.
Misra’s algorithm uses a marker that travels through the network. The marker carries
informations and modifies it depending on the internal state of the node where it currently is.
Once a threshold is reached in the information carried by the marker the distributed computation taking place in the network of nodes is considered terminated.

Implemented :

- Rudimentary simulation of a distributed system
- Simple FIFO messaging system
- Misra algorithm


Please read the "User Guide" section of the pdf for instructions to run the program.
