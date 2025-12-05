"""
Driver Interface Base Class

This module defines the base interface that all drivers must implement.
Drivers are modules that extend the assistant's functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DriverInterface(ABC):
    """
    Base class for all driver modules.
    
    All drivers must inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, version: str, description: str):
        """
        Initialize the driver.
        
        Args:
            name: The name of the driver
            version: Version string (e.g., "1.0.0")
            description: Brief description of what the driver does
        """
        self.name = name
        self.version = version
        self.description = description
        self.enabled = False
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the driver. Called when the driver is loaded.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self, command: str, *args, **kwargs) -> Any:
        """
        Execute a command using this driver.
        
        Args:
            command: The command to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Any: Result of the command execution
        """
        pass
    
    @abstractmethod
    def get_commands(self) -> Dict[str, str]:
        """
        Get a list of available commands for this driver.
        
        Returns:
            Dict[str, str]: Dictionary mapping command names to descriptions
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """
        Shutdown the driver. Called when the driver is unloaded.
        
        Returns:
            bool: True if shutdown successful, False otherwise
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get driver information.
        
        Returns:
            Dict[str, str]: Dictionary with driver metadata
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled,
            "initialized": self.initialized
        }
