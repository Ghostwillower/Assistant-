"""
System Info Driver

Provides system information capabilities.
"""

import platform
import sys
from driver_interface import DriverInterface
from typing import Dict, Any


class SystemInfoDriver(DriverInterface):
    """
    Driver for retrieving system information.
    """
    
    def __init__(self):
        super().__init__(
            name="SystemInfo",
            version="1.0.0",
            description="System information retrieval"
        )
    
    def initialize(self) -> bool:
        """
        Initialize the system info driver.
        
        Returns:
            bool: True if successful
        """
        print("System Info driver initialized")
        return True
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        """
        Execute a system info command.
        
        Args:
            command: Command to execute
            *args: Arguments for the command
            
        Returns:
            System information
        """
        if command == "os":
            return self._get_os_info()
        elif command == "python":
            return self._get_python_info()
        elif command == "platform":
            return self._get_platform_info()
        elif command == "all":
            return self._get_all_info()
        else:
            return f"Unknown command: {command}"
    
    def get_commands(self) -> Dict[str, str]:
        """
        Get available system info commands.
        
        Returns:
            Dict[str, str]: Command descriptions
        """
        return {
            "os": "Get operating system information",
            "python": "Get Python version information",
            "platform": "Get platform details",
            "all": "Get all system information"
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the system info driver.
        
        Returns:
            bool: True if successful
        """
        print("System Info driver shutdown")
        return True
    
    def _get_os_info(self) -> str:
        """Get operating system information"""
        return f"Operating System: {platform.system()} {platform.release()}"
    
    def _get_python_info(self) -> str:
        """Get Python version information"""
        return f"Python Version: {sys.version}"
    
    def _get_platform_info(self) -> str:
        """Get platform information"""
        return (f"Platform: {platform.platform()}\n"
                f"Machine: {platform.machine()}\n"
                f"Processor: {platform.processor()}")
    
    def _get_all_info(self) -> str:
        """Get all system information"""
        info = []
        info.append("=== System Information ===")
        info.append(f"System: {platform.system()}")
        info.append(f"Release: {platform.release()}")
        info.append(f"Version: {platform.version()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append(f"Platform: {platform.platform()}")
        info.append(f"\nPython Version: {sys.version}")
        info.append(f"Python Implementation: {platform.python_implementation()}")
        
        return "\n".join(info)
