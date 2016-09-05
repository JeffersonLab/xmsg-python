# coding=utf-8

import unittest

from sets import Set
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.sys.regdis.xMsgRegDatabase import xMsgRegDatabase
from xmsg.data import xMsgRegistration_pb2


def new_registration(topic, name, host):
    reg_info = xMsgRegistration_pb2.xMsgRegistration()
    reg_info.domain = topic.domain()
    reg_info.subject = topic.subject()
    reg_info.type = topic.type()
    reg_info.name = name
    reg_info.description = "some test description..."
    reg_info.host = host
    reg_info.port = 8000
    return reg_info


class TestXMsgRegDatabase(unittest.TestCase):
    topic0 = xMsgTopic.build("test_domain_0", "test_subject_0", "test_type_0")
    topic1 = xMsgTopic.build("test_domain_1", "test_subject_1", "test_type_1")
    topic2 = xMsgTopic.build("test_domain_2", "test_subject_2", "test_type_2")
    topic3 = xMsgTopic.build("test_domain_3", "test_subject_3", "test_type_3")

    reg1 = new_registration(topic0, "name0", "10.2.2.1")
    asimov1 = new_registration(topic0, "asimov", "10.2.2.1")
    asimov2 = new_registration(topic0, "asimov", "10.2.2.2")
    bradbury1 = new_registration(topic0, "bradbury", "10.2.2.1")
    bradbury2 = new_registration(topic0, "bradbury", "10.2.2.2")
    twain1 = new_registration(topic1, "twain", "10.2.2.1")
    twain2 = new_registration(topic1, "twain", "10.2.2.2")
    brando = new_registration(topic2, "brando", "10.2.2.2")
    tolkien = new_registration(topic3, "tolkien", "10.2.2.1")

    topic = "test_domain:test_subject:test_type"

    def setUp(self):
        self.db = xMsgRegDatabase()

    def test_empty_db(self):
        self.assertIsInstance(self.db.all(), list) and not self.db.all()

    def test_register_first_topic_creates_first_topic(self):
        self.db.register(self.reg1)

        self.assertEqual(self.db.get(self.topic0),
                         Set([self.reg1.SerializeToString()]))

    def test_add_next_registration_of_first_topic(self):
        self.db.register(self.twain1)
        self.db.register(self.twain2)
        test_case = self.db.get(self.topic1)

        self.assertEqual(len(test_case), 2)
        self.assertEqual(test_case,
                         Set([self.twain1.SerializeToString(),
                              self.twain2.SerializeToString()]))

    def test_add_first_registration_new_topic(self):
        self.db.register(self.asimov1)
        self.db.register(self.bradbury1)
        self.db.register(self.twain1)
        self.db.register(self.tolkien)

        self.assertEqual(len(self.db.all()), 3)
        self.assertEqual(self.db.all(),
                         [str(self.topic0),
                          str(self.topic1),
                          str(self.topic3)])

        test_case = self.db.get(self.topic0)
        self.assertEqual(test_case, Set([self.asimov1.SerializeToString(),
                                         self.bradbury1.SerializeToString()]))

        test_case = self.db.get(self.topic1)
        self.assertEqual(test_case, Set([self.twain1.SerializeToString()]))

        test_case = self.db.get(self.topic3)
        self.assertEqual(test_case, Set([self.tolkien.SerializeToString()]))

    def add_duplicated_registration_does_nothing(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.bradbury1)
        self.db.register(self.bradbury1)

        test_case = self.db.get(self.topic0)
        self.assertEqual(test_case,
                         Set([self.asimov1.SerializeToString(),
                              self.bradbury1.SerializeToString()]))

    def test_remove_register_with_only_topic_db_one_element(self):
        self.db.clear()
        self.db.register(self.reg1)
        self.db.remove(self.reg1)

        self.assertIsNone(self.db.get(self.topic0))
        self.assertEqual(self.db.all(), [])

    def test_remove_register_with_only_topic_with_several_element(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.asimov2)
        self.db.register(self.bradbury1)
        self.db.remove(self.asimov2)

        test_case = self.db.find("test_domain_0", "test_subject_0", "test_type_0")

        self.assertEqual(test_case, Set([self.asimov1.SerializeToString(),
                                         self.bradbury1.SerializeToString()]))

    def test_remove_register_with_topic_with_one_element(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.twain1)
        self.db.register(self.twain2)
        self.db.remove(self.asimov1)

        test_case = self.db.find("test_domain_1", "test_subject_1", "test_type_1")
        self.assertEqual(self.db.all(), [str(self.topic1)])
        self.assertEqual(test_case, Set([self.twain1.SerializeToString(),
                                         self.twain2.SerializeToString()]))

    def test_remove_register_with_topic_db_several_element(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.asimov2)
        self.db.register(self.bradbury1)
        self.db.register(self.twain1)
        self.db.register(self.twain2)
        self.db.remove(self.bradbury1)

        self.assertEqual(self.db.all(), [str(self.topic0), str(self.topic1)])

        self.assertEqual(self.db.get("test_domain_0:test_subject_0:test_type_0"),
                         Set([self.asimov1.SerializeToString(),
                              self.asimov2.SerializeToString()]))

        self.assertEqual(self.db.get("test_domain_1:test_subject_1:test_type_1"),
                         Set([self.twain1.SerializeToString(),
                              self.twain2.SerializeToString()]))

    def test_remove_missing_registration_does_nothing(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.asimov2)

        self.db.remove(self.bradbury1)

        self.assertEqual(self.db.get(str(self.topic0)),
                         Set([self.asimov1.SerializeToString(),
                              self.asimov2.SerializeToString()]))

    def test_remove_by_host(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.asimov2)
        self.db.register(self.bradbury1)
        self.db.register(self.bradbury2)
        self.db.register(self.twain1)
        self.db.register(self.twain2)

        self.db.remove_by_host("10.2.2.1")

        self.assertEqual(self.db.get("test_domain_0:test_subject_0:test_type_0"),
                         Set([self.asimov2.SerializeToString(),
                              self.bradbury2.SerializeToString()]))
        self.assertEqual(self.db.get("test_domain_1:test_subject_1:test_type_1"),
                         Set([self.twain2.SerializeToString()]))

    def test_get_by_domain(self):
        self.db.clear()
        self.db.register(self.reg1)

        test_case = self.db.find(self.reg1.domain)
        self.assertEqual(test_case, Set([self.reg1.SerializeToString()]))

    def test_get_by_domain_and_subject(self):
        self.db.clear()
        self.db.register(self.reg1)

        test_case = self.db.find(self.reg1.domain, self.reg1.subject)
        self.assertEqual(test_case, Set([self.reg1.SerializeToString()]))

    def test_find_Set_by_topic(self):
        self.db.clear()
        self.db.register(self.reg1)

        self.assertEqual(self.db.get(self.topic0),
                         Set([self.reg1.SerializeToString()]))
        self.assertIsNone(self.db.get(self.topic1))

    def test_find_unregistered_topic_returns_none(self):
        self.db.clear()
        self.db.register(self.asimov1)
        self.db.register(self.bradbury2)
        self.db.register(self.brando)
        self.db.register(self.tolkien)

        self.assertIsNone(self.db.find(str(self.topic1)))

if __name__ == "__main__":
    unittest.main()
