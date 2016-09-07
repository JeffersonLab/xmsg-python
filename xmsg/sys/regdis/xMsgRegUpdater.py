#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import threading

from xmsg.core.xMsgUtil import xMsgUtil


__author__ = 'royarzun'


class xMsgRegUpdater(threading.Thread):
    """This is a thread that periodically updates xMsg front-end registration
    database with passed publishers and subscribers database contents. These
    passed databases (i.e. references) are xMsgNode resident databases,
    defined within the xMsgRegistrar class. This class will be instantiated
    by the xMsgRegistrar constructor executed by the xMsgNode:

    This class inherits from xMsgRegDrive where xMsg database communication
    methods are defined.

    Attributes:
        driver (xMsgRegDriver): registration driver
        publishers_db (xMsgRegDatabase): publishers database
        subscribers_db (xMsgRegDatabase): subscribers database
        name (String): name of updater instance
    """

    def __init__(self, driver, publishers_db, subscribers_db):
        super(xMsgRegUpdater, self).__init__()
        self.driver = driver
        self.publishers_db = publishers_db
        self.subscribers_db = subscribers_db
        self.name = "%s_registration_updater" % xMsgUtil.host_to_ip("localhost")
        self.daemon = True

        # Lock used to lock xMsgNode databases access
        self.lock = threading.Lock()

    def _update_frontend_task(self):
        # update FE publishers database
        self.lock.acquire()
        try:
            for topic in self.publishers_db.all():
                self.driver.register_fe(topic,
                                        self.publishers_db.get(topic),
                                        True)
                xMsgUtil.sleep(0.5)

        finally:
            self.lock.release()

        # update FE subscribers database
        self.lock.acquire()
        try:
            for topic in self.subscribers_db.all():
                self.driver.register_fe(topic,
                                        self.subscribers_db.get(topic),
                                        False)
                xMsgUtil.sleep(0.5)

        finally:
            self.lock.release()

        xMsgUtil.sleep(5)

    def run(self):
        """xMsgRegUpdater thread method to update the frontend registration db

        Every cicle will try to push the registration information into the
        frontend registration database. The defined algorithm for this task is
        described below.

        Method description:
        ::
            while thread is alive:
                for each topic in subscribers_database:
                    register_in_fe(topic)

                sleep .5 seconds

                for each topic in subscribers_database:
                    register_in_fe(topic)

                sleep .5 seconds
        """
        while True and threading.currentThread().is_alive():
            try:
                self._update_frontend_task()

            except:
                return
