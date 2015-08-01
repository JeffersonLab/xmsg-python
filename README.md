# xMsg for python

### System Requirements

So far tested in:
*  Ubuntu 14.10
*  Fedora 22
*  OSX Yosemite

```sh
$ # Ubuntu:
$ sudo aptitude install libzmq3-dev virtualenv csh
$ # Fedora 22:
$ sudo dnf install virtualenv tcsh zeromq3-devel
```

### Installing xMsg

To install xMsg in your system run:

```sh
$ sudo python setup.py install
```

This will install the xMsg package in the system libraries, and will copy the
xmsg scripts in the /usr/bin/ directory.

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
$ ./bin/unix/px_publisher <size_of_array_to_publish> <fe_host_if_any>
```

```sh
$ ./bin/unix/px_subscriber <fe_host_if_any>
```

You can find the publisher and subscriber source code at the examples package

---

### Performance tests

User can run performance tests for benchmark purposes. The way of running this tests its the following.
First of all you need to start a xMsg proxy or registrar:

```sh
$ python xmsg/xsys/xMsgRegistrar.py
$ # or
$ python xmsg/xsys/xMsgProxy.py
```

Starts the performance test subscriber instance, this instance will print the tests results in the console, if you add the "--csv-output" the instance will print the output in csv format.

```sh
$ python tests/perf/LocalThroughput.py <bind_to> [--csv-output]
```

And now the publisher, you can give arguments to run the publisher process:

```sh
$ python tests/perf/RemoteThroughput.py <bind_to> <message_size> <number_of_messages_to_publish>
```

You can also call the remoteRunner to run test more automatically

```sh
$ python tests/perf/RemoteThroughputRunner.py <bind_to> <message_size> <start-message-count> <final-message-count> <step>
```
