import unittest
import elasticd
import elasticd.ext.sqlite_datastore

class TestVarnishDriver(unittest.TestCase):

    def test_driver_load(self):
        self.assertEqual('Hello', 'Hello')
        elasticd.startup()

if __name__ == '__main__':
    unittest.main()
