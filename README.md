# xMsg 2.3.1 for python

### System Requirements

```sh
$ # Ubuntu:
$ sudo aptitude install libzmq3-dev
$ # OSX
$ brew install zmq
```

### Installing xMsg

To install xmsg-python in your system run:

```sh
$ ./setup.py install
```

### Quick Start
TODO: Quick Start section


### Examples

To run the examples:

```sh
$ # start a xMsgNode process using the scripts
$ # in the scripts folder
$ px_node
$ # or an xMsgProxy process 
$ # in the scripts folder
$ px_proxy
```

then run the publisher and subscriber scripts:

```sh
$ ./bin/unix/px_publisher <size_of_array_to_publish>
```

```sh
$ ./bin/unix/px_subscriber
```

You can find the publisher and subscriber source code at the examples package

---
