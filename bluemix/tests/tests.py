import  unittest
from app import reverseGeocode, getAddressDetails
import googlemaps

class Test(unittest.TestCase):
    def test(self):
        result = reverseGeocode(19.1031, 72.8467)
        ans = getAddressDetails(result)
        self.assertEqual(ans[0], "Mumbai")
        self.assertEqual(ans[1], "MH")
        self.assertEqual(ans[2], "IN")

if __name__ == '__main__':
    unittest.main()