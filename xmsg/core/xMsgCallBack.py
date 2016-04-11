# coding=utf-8


class xMsgCallBack(object):

    def callback(self, msg):
        """xMsg user defined callback interface: A.K.A: what to do with data
        received

        Args:
            msg (xMsgMessage): transient message object

        Returns:
            callback_message (xMsgMessage): message with the callback result
        """
        raise NotImplementedError("User needs to define callback")
