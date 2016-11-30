# xmsg for python [![BuildStatus](https://travis-ci.org/JeffersonLab/xmsg_python.svg?branch=dev)](https://travis-ci.org/JeffersonLab/xmsg_python)

xMsg is a lightweight, yet full featured publish/subscribe messaging system, presenting asynchronous publish/subscribe inter-process communication protocol: an API layer in Java, Python and C++.

xMsg provides in memory registration database that is used to register xMsg actors (i.e. publishers and subscribers). Hence, xMsg API includes methods for registering and discovering publishers and subscribers. This makes xMsg a suitable framework to build symmetric SOA based applications. For example a services that has a message to publishing can check to see if there are enough subscribers of this particular message type.

To solve dynamic discovery problem in pub/sub environment the need of a proxy server is unavoidable. xMsg is using 0MQ socket libraries and borrows 0MQ proxy, which is a simple stateless message switch to address mentioned dynamic discovery problem.

xMsg stores proxy connection objects internally in a connection pool for efficiency reasons. To avoid proxy connection concurrency, thus achieving maximum performance, connection objects are not shared between threads. Each xMsg actor tread will reuse an available connection object, or create a new proxy connection if it is not available in the pool.

xMsg publisher can send a message of any topic. xMsg subscribers subscribe to abstract topics and provide callbacks to handle messages as they arrive, in a so called subscribe-and-forget mode. Neither publisher nor subscriber knows of each others existence. Thus publishers and subscribers are completely independent of each others. Yet, for a proper communication they need to establish some kind of relationship or binding, and that binding is the communication or message topic. Note that multiple xMsg actors can communicate without interfering with each other via simple topic naming conventions. xMsg topic convention defines three parts: domain, subject, and type, presented by the xMsgTopic class.

xMsg subscriber callbacks (implementing xMsgCallBack interface) will run in a separate thread. For that reason xMsg provides a thread pool, simplifying the job of a user. Note that user provided callback routines must be thread safe and/or thread enabled.


### System Requirements

```sh
$ # Ubuntu:
$ sudo aptitude install libzmq3-dev
$ sudo aptitude install python-dev
$ # OSX
$ brew install zmq
```

### Installing xmsg

To install xmsg-python in your system run:

```sh
$ pip install -r requirements # install xmsg python dependencies
$ ./setup.py install
```

### Quick Start
TODO: Quick Start section


### Examples

To run the examples:

```sh
$ # start a xMsgNode process using the scripts
$ px_node
$ # or an xMsgProxy process 
$ # in the scripts folder
$ px_proxy
```

then run the publisher and subscriber scripts:

```sh
$ px_publisher <size_of_array_to_publish>
```

```sh
$ px_subscriber
```

You can find the publisher and subscriber source code at the examples package

---

For more details and API method signatures check the Javadoc.

For assistance contact authors:

* Vardan Gyurjyan    (<gurjyan@jlab.org>)
* Sebastián Mancilla (<smancill@jlab.org>)
* Ricardo Oyarzún    (<oyarzun@jlab.org>)
