import sending
import looper
import login 
import unittest



class TestLogin(unittest.TestCase):

    def testCheckReturn0(self):
        returned = login.check(3697,'p',1)
        self.assertEqual(0, returned)

    def testCheckReturn22(self):
        returned = login.check(3573,'c',4)
        self.assertEqual(22, returned)

    def testCheckNoLecture(self):
        returned = login.check(9999,'c',1)
        self.assertEqual(returned, 99999)

    def testCheckNoType(self):
        returned = login.check(3573,'p',1)
        self.assertEqual(returned,99999)
    
    def testCheckNoGroup(self):
        returned = login.check(3573,'c',19)
        self.assertEqual(returned,99999)


class TestLooper(unittest.TestCase):
    
    def testProcessIfNoPlaces(self):
        returned = looper.process((7,3697,'p',1,None,'','ktos@jakis.serwer','ktos@jakis.jabber'))
        self.assertFalse(returned)

    def testProcessIf22Places(self):
        ID = 333
        returned = looper.process((ID,3573,'c',1,None,'','ktos@jakis.serwer','ktos@jakis.jabber'))
        self.assertEqual(returned, ID)
    


if __name__ == '__main__':
    unittest.main()

