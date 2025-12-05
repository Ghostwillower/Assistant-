"""
Template Driver

This is a template for creating new drivers. Copy this file and modify it
to create your own custom driver for the Desktop Assistant.

Usage:
1. Copy this file to the drivers/ directory
2. Rename it with '_driver.py' suffix (e.g., 'my_custom_driver.py')
3. Update the class name and implementation
4. Implement all required methods
5. The driver will be automatically discovered and loaded
"""

from driver_interface import DriverInterface
from typing import Dict, Any


class TemplateDriver(DriverInterface):
    """
    Template driver - replace with your driver description.
    """
    
    def __init__(self):
        """
        Initialize your driver.
        Update name, version, and description.
        """
        super().__init__(
            name="TemplateName",           # Driver name (shown in UI)
            version="1.0.0",                # Version string
            description="Description here"  # Brief description
        )
        # Add your custom initialization here
        self.custom_data = {}
    
    def initialize(self) -> bool:
        """
        Initialize the driver. Called when the driver is loaded.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Add your initialization code here
            # For example: connect to external service, load resources, etc.
            print(f"{self.name} driver initialized")
            return True
        except Exception as e:
            print(f"Error initializing {self.name}: {str(e)}")
            return False
    
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
        # Route commands to appropriate methods
        if command == "example_command":
            return self._example_command(args[0] if args else "")
        elif command == "another_command":
            return self._another_command(args[0] if args else "")
        else:
            return f"Unknown command: {command}"
    
    def get_commands(self) -> Dict[str, str]:
        """
        Get a list of available commands for this driver.
        
        Returns:
            Dict[str, str]: Dictionary mapping command names to descriptions
        """
        return {
            "example_command": "Description of example command",
            "another_command": "Description of another command",
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the driver. Called when the driver is unloaded.
        
        Returns:
            bool: True if shutdown successful, False otherwise
        """
        try:
            # Add your cleanup code here
            # For example: close connections, save state, etc.
            print(f"{self.name} driver shutdown")
            return True
        except Exception as e:
            print(f"Error shutting down {self.name}: {str(e)}")
            return False
    
    # Private methods for command implementations
    
    def _example_command(self, input_data: str) -> str:
        """
        Example command implementation.
        
        Args:
            input_data: Input from the user
            
        Returns:
            str: Result of the command
        """
        try:
            # Implement your command logic here
            return f"Processed: {input_data}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _another_command(self, input_data: str) -> str:
        """
        Another command implementation.
        
        Args:
            input_data: Input from the user
            
        Returns:
            str: Result of the command
        """
        try:
            # Implement your command logic here
            return f"Result: {input_data}"
        except Exception as e:
            return f"Error: {str(e)}"


# Example: Driver that interacts with external programs
"""
class ExternalProgramDriver(DriverInterface):
    
    def __init__(self):
        super().__init__("ExternalApp", "1.0.0", "Controls external application")
        self.process = None
    
    def initialize(self):
        import subprocess
        # Start external program
        # self.process = subprocess.Popen(['external-app'])
        return True
    
    def execute(self, command, *args, **kwargs):
        if command == "send_command":
            # Send command to external program
            pass
        return "Command executed"
    
    def get_commands(self):
        return {"send_command": "Send command to external app"}
    
    def shutdown(self):
        if self.process:
            self.process.terminate()
        return True
"""
