"""
Assistant Core

The main logic for the desktop assistant application.
"""

import json
import os
from typing import Dict, Any, Optional
from driver_manager import DriverManager


class AssistantCore:
    """
    Core assistant application logic.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the assistant core.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.driver_manager = DriverManager(self.config.get("drivers_directory", "drivers"))
        self.running = False
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Dict[str, Any]: Default configuration
        """
        return {
            "app_name": "Desktop Assistant",
            "version": "1.0.0",
            "drivers_directory": "drivers",
            "auto_load_drivers": True,
            "enabled_drivers": [],
            "window_settings": {
                "width": 800,
                "height": 600,
                "title": "Desktop Assistant"
            }
        }
    
    def save_config(self):
        """
        Save current configuration to file.
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
    
    def start(self):
        """
        Start the assistant and load drivers.
        """
        print(f"Starting {self.config['app_name']} v{self.config['version']}")
        self.running = True
        
        if self.config.get("auto_load_drivers", True):
            self._auto_load_drivers()
    
    def _auto_load_drivers(self):
        """
        Automatically discover and load enabled drivers.
        """
        discovered = self.driver_manager.discover_drivers()
        enabled_drivers = self.config.get("enabled_drivers", [])
        
        # Load enabled drivers
        for module_name in discovered:
            if not enabled_drivers or module_name in enabled_drivers:
                self.driver_manager.load_driver(module_name)
    
    def stop(self):
        """
        Stop the assistant and shutdown all drivers.
        """
        print("Stopping assistant...")
        self.driver_manager.shutdown_all()
        self.running = False
    
    def execute_command(self, driver_name: str, command: str, *args, **kwargs):
        """
        Execute a command on a driver.
        
        Args:
            driver_name: Name of the driver
            command: Command to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Result of command execution
        """
        return self.driver_manager.execute_command(driver_name, command, *args, **kwargs)
    
    def get_loaded_drivers(self) -> Dict:
        """
        Get information about all loaded drivers.
        
        Returns:
            Dict: Dictionary of driver information
        """
        drivers = self.driver_manager.get_all_drivers()
        return {name: driver.get_info() for name, driver in drivers.items()}
    
    def get_driver_commands(self, driver_name: str) -> Optional[Dict[str, str]]:
        """
        Get available commands for a driver.
        
        Args:
            driver_name: Name of the driver
            
        Returns:
            Optional[Dict[str, str]]: Command dictionary or None
        """
        driver = self.driver_manager.get_driver(driver_name)
        if driver:
            return driver.get_commands()
        return None
