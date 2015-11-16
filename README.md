# xMsg 2.3 for python

### System Requirements

So far tested in:
*  Ubuntu 15.10
*  OSX El Capitan

```sh
$ # Ubuntu:
$ sudo aptitude install libzmq3-dev
$ # OSX
$ brew install zmq
```

### Installing xMsg

To install xMsg in your system run:

```sh
$ ./setup.py install
```

This will install the xMsg package in the system libraries, and will copy the
xmsg scripts in the /usr/bin/ directory.

For development use:

```sh
$ python setup.py develop
```

this command installs the package (in the xmsg source folder) in a way that allows you to conveniently
edit your code after its installed to the (virtual) environment and have the changes take effect
immediately.


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
