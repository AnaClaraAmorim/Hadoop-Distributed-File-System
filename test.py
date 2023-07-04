import unittest
from distributed import Node, DistributedFileSystem
import threading
import socket

class TestDistributed(unittest.TestCase):

    def setUp(self):
        self.token = "test_token"
        self.host = "localhost"
        self.port = 6000
        self.node = Node(self.host, self.port, self.token)

        self.dfs = DistributedFileSystem()
        self.dfs.add_node(self.node)

    def tearDown(self):
        self.node.server.close()

    def test_store_and_retrieve_data(self):
        test_key = "test_key"
        test_value = "test_value"
        self.node.store_data(test_key, test_value)

        retrieved_value = self.node.retrieve_data(test_key)
        self.assertEqual(test_value, retrieved_value)

    def test_distribute_and_retrieve_data(self):
        test_key = "test_key_dfs"
        test_value = "test_value_dfs"
        self.dfs.distribute_data(self.token, test_key, test_value)

        retrieved_value = self.dfs.retrieve_data(self.token, test_key)
        self.assertEqual(test_value, retrieved_value)

if __name__ == '__main__':
    unittest.main()