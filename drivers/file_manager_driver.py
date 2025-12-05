"""
File Manager Driver

Provides file system operations capabilities.
"""

import os
from driver_interface import DriverInterface
from typing import Dict, Any


class FileManagerDriver(DriverInterface):
    """
    Driver for basic file system operations.
    """
    
    def __init__(self):
        super().__init__(
            name="FileManager",
            version="1.0.0",
            description="File system operations"
        )
        self.current_dir = os.getcwd()
    
    def initialize(self) -> bool:
        """
        Initialize the file manager driver.
        
        Returns:
            bool: True if successful
        """
        print("File Manager driver initialized")
        return True
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        """
        Execute a file manager command.
        
        Args:
            command: Command to execute
            *args: Arguments for the command
            
        Returns:
            Result of the operation
        """
        if command == "list":
            return self._list_files(args[0] if args else ".")
        elif command == "read":
            return self._read_file(args[0] if args else "")
        elif command == "create":
            return self._create_file(args[0] if args else "")
        elif command == "exists":
            return self._file_exists(args[0] if args else "")
        elif command == "cwd":
            return self._get_cwd()
        else:
            return f"Unknown command: {command}"
    
    def get_commands(self) -> Dict[str, str]:
        """
        Get available file manager commands.
        
        Returns:
            Dict[str, str]: Command descriptions
        """
        return {
            "list": "List files in directory (e.g., '.' or '/path')",
            "read": "Read file contents (e.g., 'file.txt')",
            "create": "Create a new file (e.g., 'newfile.txt')",
            "exists": "Check if file exists (e.g., 'file.txt')",
            "cwd": "Get current working directory"
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the file manager driver.
        
        Returns:
            bool: True if successful
        """
        print("File Manager driver shutdown")
        return True
    
    def _list_files(self, path: str) -> str:
        """List files in a directory"""
        try:
            if not path or path == "":
                path = "."
            
            files = os.listdir(path)
            if not files:
                return f"Directory '{path}' is empty"
            
            result = f"Contents of '{os.path.abspath(path)}':\n"
            for item in sorted(files):
                full_path = os.path.join(path, item)
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                result += f"  [{item_type}] {item}\n"
            return result.strip()
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def _read_file(self, filename: str) -> str:
        """Read contents of a file"""
        try:
            if not filename:
                return "Error: No filename provided"
            
            if not os.path.exists(filename):
                return f"Error: File '{filename}' not found"
            
            if os.path.isdir(filename):
                return f"Error: '{filename}' is a directory"
            
            with open(filename, 'r') as f:
                content = f.read()
            
            return f"Contents of '{filename}':\n{content}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _create_file(self, filename: str) -> str:
        """Create a new empty file"""
        try:
            if not filename:
                return "Error: No filename provided"
            
            if os.path.exists(filename):
                return f"Error: File '{filename}' already exists"
            
            with open(filename, 'w') as f:
                f.write("")
            
            return f"Created file: {os.path.abspath(filename)}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    def _file_exists(self, filename: str) -> str:
        """Check if a file exists"""
        if not filename:
            return "Error: No filename provided"
        
        exists = os.path.exists(filename)
        return f"File '{filename}' {'exists' if exists else 'does not exist'}"
    
    def _get_cwd(self) -> str:
        """Get current working directory"""
        return f"Current directory: {os.getcwd()}"
