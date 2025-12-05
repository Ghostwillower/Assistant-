"""
Driver Manager

This module handles the discovery, loading, and management of driver modules.
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Optional
from driver_interface import DriverInterface


class DriverManager:
    """
    Manages driver loading, initialization, and lifecycle.
    """
    
    def __init__(self, drivers_directory: str = "drivers"):
        """
        Initialize the driver manager.
        
        Args:
            drivers_directory: Path to directory containing driver modules
        """
        self.drivers_directory = drivers_directory
        self.drivers: Dict[str, DriverInterface] = {}
        self.loaded_modules = {}
        
        # Ensure drivers directory exists
        if not os.path.exists(drivers_directory):
            os.makedirs(drivers_directory)
            
        # Add drivers directory to Python path
        if drivers_directory not in sys.path:
            sys.path.insert(0, os.path.abspath(drivers_directory))
    
    def discover_drivers(self) -> List[str]:
        """
        Discover available driver modules in the drivers directory.
        
        Returns:
            List[str]: List of discovered driver module names
        """
        discovered = []
        
        if not os.path.exists(self.drivers_directory):
            return discovered
        
        for filename in os.listdir(self.drivers_directory):
            if filename.endswith("_driver.py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                discovered.append(module_name)
        
        return discovered
    
    def load_driver(self, module_name: str) -> bool:
        """
        Load a driver module by name.
        
        Args:
            module_name: Name of the module to load (without .py extension)
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            # Import the module
            module_path = os.path.join(self.drivers_directory, f"{module_name}.py")
            
            if not os.path.exists(module_path):
                print(f"Driver module not found: {module_path}")
                return False
            
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                self.loaded_modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Find the driver class in the module
                driver_instance = None
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if (isinstance(item, type) and 
                        issubclass(item, DriverInterface) and 
                        item is not DriverInterface):
                        driver_instance = item()
                        break
                
                if driver_instance:
                    # Initialize the driver
                    if driver_instance.initialize():
                        driver_instance.enabled = True
                        driver_instance.initialized = True
                        self.drivers[driver_instance.name] = driver_instance
                        print(f"Loaded driver: {driver_instance.name} v{driver_instance.version}")
                        return True
                    else:
                        print(f"Failed to initialize driver: {module_name}")
                        return False
                else:
                    print(f"No valid driver class found in module: {module_name}")
                    return False
            else:
                print(f"Failed to load module spec: {module_name}")
                return False
                
        except Exception as e:
            print(f"Error loading driver {module_name}: {str(e)}")
            return False
    
    def unload_driver(self, driver_name: str) -> bool:
        """
        Unload a driver by name.
        
        Args:
            driver_name: Name of the driver to unload
            
        Returns:
            bool: True if unloaded successfully, False otherwise
        """
        if driver_name in self.drivers:
            driver = self.drivers[driver_name]
            driver.shutdown()
            driver.enabled = False
            driver.initialized = False
            del self.drivers[driver_name]
            print(f"Unloaded driver: {driver_name}")
            return True
        return False
    
    def get_driver(self, driver_name: str) -> Optional[DriverInterface]:
        """
        Get a driver instance by name.
        
        Args:
            driver_name: Name of the driver
            
        Returns:
            Optional[DriverInterface]: Driver instance or None if not found
        """
        return self.drivers.get(driver_name)
    
    def get_all_drivers(self) -> Dict[str, DriverInterface]:
        """
        Get all loaded drivers.
        
        Returns:
            Dict[str, DriverInterface]: Dictionary of all loaded drivers
        """
        return self.drivers.copy()
    
    def execute_command(self, driver_name: str, command: str, *args, **kwargs):
        """
        Execute a command on a specific driver.
        
        Args:
            driver_name: Name of the driver
            command: Command to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Result of command execution or error message
        """
        driver = self.get_driver(driver_name)
        if driver and driver.enabled:
            try:
                return driver.execute(command, *args, **kwargs)
            except Exception as e:
                return f"Error executing command: {str(e)}"
        else:
            return f"Driver '{driver_name}' not found or not enabled"
    
    def shutdown_all(self):
        """
        Shutdown all loaded drivers.
        """
        for driver_name in list(self.drivers.keys()):
            self.unload_driver(driver_name)
