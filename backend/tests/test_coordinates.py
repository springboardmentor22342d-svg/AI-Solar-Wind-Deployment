import unittest
import sys
import os

# Add the backend directory to sys.path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.coordinates import Coordinate, validate_coordinates, create_coordinate

class TestCoordinates(unittest.TestCase):
    def test_valid_coordinates(self):
        self.assertTrue(validate_coordinates(20.2961, 85.8245))
        coord = create_coordinate(20.2961, 85.8245)
        self.assertEqual(coord.latitude, 20.2961)
        self.assertEqual(coord.longitude, 85.8245)

    def test_invalid_latitude(self):
        self.assertFalse(validate_coordinates(91.0, 85.8245))
        self.assertFalse(validate_coordinates(-91.0, 85.8245))
        
        with self.assertRaises(ValueError):
            create_coordinate(91.0, 85.8245)
            
        with self.assertRaises(ValueError):
            create_coordinate(-91.0, 85.8245)

    def test_invalid_longitude(self):
        self.assertFalse(validate_coordinates(20.2961, 181.0))
        self.assertFalse(validate_coordinates(20.2961, -181.0))
        
        with self.assertRaises(ValueError):
            create_coordinate(20.2961, 181.0)
            
        with self.assertRaises(ValueError):
            create_coordinate(20.2961, -181.0)

if __name__ == '__main__':
    unittest.main()
