"""
Unit tests for the Driver Manager
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from driver_manager import DriverManager
from driver_interface import DriverInterface


class MockDriver(DriverInterface):
    """Mock driver for testing"""
    
    def __init__(self):
        super().__init__("MockDriver", "1.0.0", "Test driver")
    
    def initialize(self):
        return True
    
    def execute(self, command, *args, **kwargs):
        return f"Executed: {command}"
    
    def get_commands(self):
        return {"test": "Test command"}
    
    def shutdown(self):
        return True


class TestDriverManager(unittest.TestCase):
    """Test cases for DriverManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = DriverManager("drivers")
    
    def tearDown(self):
        """Clean up after tests"""
        self.manager.shutdown_all()
    
    def test_discover_drivers(self):
        """Test driver discovery"""
        discovered = self.manager.discover_drivers()
        self.assertIsInstance(discovered, list)
        # Should discover our example drivers
        self.assertIn("calculator_driver", discovered)
        self.assertIn("file_manager_driver", discovered)
        self.assertIn("system_info_driver", discovered)
    
    def test_load_driver(self):
        """Test loading a driver"""
        result = self.manager.load_driver("calculator_driver")
        self.assertTrue(result)
        self.assertIn("Calculator", self.manager.drivers)
    
    def test_get_driver(self):
        """Test retrieving a loaded driver"""
        self.manager.load_driver("calculator_driver")
        driver = self.manager.get_driver("Calculator")
        self.assertIsNotNone(driver)
        self.assertEqual(driver.name, "Calculator")
    
    def test_execute_command(self):
        """Test executing a command through the manager"""
        self.manager.load_driver("calculator_driver")
        result = self.manager.execute_command("Calculator", "add", "5+3")
        self.assertIn("8", str(result))
    
    def test_unload_driver(self):
        """Test unloading a driver"""
        self.manager.load_driver("calculator_driver")
        self.assertIn("Calculator", self.manager.drivers)
        
        result = self.manager.unload_driver("Calculator")
        self.assertTrue(result)
        self.assertNotIn("Calculator", self.manager.drivers)
    
    def test_get_all_drivers(self):
        """Test getting all loaded drivers"""
        self.manager.load_driver("calculator_driver")
        self.manager.load_driver("file_manager_driver")
        
        all_drivers = self.manager.get_all_drivers()
        self.assertIsInstance(all_drivers, dict)
        self.assertGreaterEqual(len(all_drivers), 2)


if __name__ == '__main__':
    unittest.main()
