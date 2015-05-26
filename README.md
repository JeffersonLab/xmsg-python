#xMsg for python

### System Requirements

For ubuntu:
```sh
$ sudo aptitude install libzmq3-dev virtualenv csh
```

... and the python requirements:

```sh
$ cd /path/to/xmsg-python
$ pip install -r requirements.txt
```
### Examples

To run the examples:

```sh
$ # start a xMsgNode process using the scripts
$ # in the scripts folder
$ ./scripts/unix/px_node
```

And then run the publisher and subscriber scripts:

```sh
$ ./scripts/unix/px_publisher 5 # 5 or any int number
```

```sh
$ ./scripts/unix/px_subscriber
```
