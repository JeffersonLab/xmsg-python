#xMsg for python

### System Requirements

For ubuntu (so far tested on 14.10):

```sh
$ sudo aptitude install libzmq3-dev virtualenv csh
```

### Installing xMsg

To install xMsg in your system run:

```sh
$ python setup.py install
```

For development use:

```sh
$ python setup.py develop
```

this installs the package (in the xmsg source folder) in a way that allows you to conveniently
edit your code after its installed to the (virtual) environment and have the changes take effect
immediately.


### Examples

To run the examples:

```sh
$ # start a xMsgNode process using the scripts
$ # in the scripts folder
$ ./bin/unix/px_node
```

then run the publisher and subscriber scripts:

```sh
$ ./bin/unix/px_publisher 5 # 5 or any int number
```

```sh
$ ./bin/unix/px_subscriber
```

You can find the publisher and subscriber source code at the examples package
