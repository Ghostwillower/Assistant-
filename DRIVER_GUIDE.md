# Driver Development Guide

This guide explains how to create custom drivers for the Desktop Assistant.

## What are Drivers?

Drivers are modular plugins that extend the assistant's capabilities. They act as interfaces between the assistant and external programs, services, or data sources. Each driver is a self-contained Python module that implements a standard interface.

## Driver Architecture

All drivers must inherit from the `DriverInterface` base class and implement these methods:

- `initialize()`: Set up the driver (called once when loaded)
- `execute(command, *args, **kwargs)`: Execute a command
- `get_commands()`: Return available commands
- `shutdown()`: Clean up resources (called when unloaded)

## Creating a New Driver

### Step 1: Create the Driver File

Create a new Python file in the `drivers/` directory with the suffix `_driver.py`:

```bash
drivers/my_custom_driver.py
```

### Step 2: Import Required Modules

```python
from driver_interface import DriverInterface
from typing import Dict, Any
```

### Step 3: Define Your Driver Class

```python
class MyCustomDriver(DriverInterface):
    def __init__(self):
        super().__init__(
            name="MyDriver",
            version="1.0.0",
            description="My custom driver description"
        )
```

### Step 4: Implement Required Methods

```python
def initialize(self) -> bool:
    """Initialize the driver"""
    print(f"{self.name} initialized")
    return True

def execute(self, command: str, *args, **kwargs) -> Any:
    """Execute a command"""
    if command == "my_command":
        return self._my_command(args[0] if args else "")
    return f"Unknown command: {command}"

def get_commands(self) -> Dict[str, str]:
    """Return available commands"""
    return {
        "my_command": "Description of my command"
    }

def shutdown(self) -> bool:
    """Clean up resources"""
    print(f"{self.name} shutdown")
    return True
```

### Step 5: Implement Your Logic

```python
def _my_command(self, input_data: str) -> str:
    """Private method for command implementation"""
    # Your logic here
    return f"Result: {input_data}"
```

## Example: Web Search Driver

Here's a complete example of a driver that performs web searches:

```python
from driver_interface import DriverInterface
from typing import Dict, Any
import urllib.parse

class WebSearchDriver(DriverInterface):
    def __init__(self):
        super().__init__(
            name="WebSearch",
            version="1.0.0",
            description="Web search functionality"
        )
        self.search_engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q="
        }
    
    def initialize(self) -> bool:
        print("Web Search driver initialized")
        return True
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        if command == "search":
            query = args[0] if args else ""
            engine = kwargs.get('engine', 'google')
            return self._search(query, engine)
        elif command == "list_engines":
            return self._list_engines()
        return f"Unknown command: {command}"
    
    def get_commands(self) -> Dict[str, str]:
        return {
            "search": "Search the web (provide query)",
            "list_engines": "List available search engines"
        }
    
    def shutdown(self) -> bool:
        print("Web Search driver shutdown")
        return True
    
    def _search(self, query: str, engine: str) -> str:
        if engine not in self.search_engines:
            return f"Unknown search engine: {engine}"
        
        encoded_query = urllib.parse.quote(query)
        url = self.search_engines[engine] + encoded_query
        return f"Search URL: {url}"
    
    def _list_engines(self) -> str:
        engines = ", ".join(self.search_engines.keys())
        return f"Available engines: {engines}"
```

## Driver Best Practices

### 1. Error Handling

Always handle exceptions gracefully:

```python
def execute(self, command: str, *args, **kwargs) -> Any:
    try:
        # Your logic
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### 2. Resource Management

Clean up resources in the `shutdown()` method:

```python
def shutdown(self) -> bool:
    try:
        if self.connection:
            self.connection.close()
        return True
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")
        return False
```

### 3. Documentation

Document your commands clearly:

```python
def get_commands(self) -> Dict[str, str]:
    return {
        "command_name": "Clear description with example input format",
        "another_cmd": "What it does and expected parameters"
    }
```

### 4. Input Validation

Validate user input:

```python
def _my_command(self, input_data: str) -> str:
    if not input_data:
        return "Error: Input required"
    
    if not input_data.isdigit():
        return "Error: Input must be numeric"
    
    # Process valid input
    return f"Processed: {input_data}"
```

## Testing Your Driver

### Manual Testing

1. Place your driver in `drivers/` directory
2. Add driver name to `config.json` enabled_drivers list
3. Run the application: `python main.py`
4. Select your driver from the GUI
5. Test each command

### Automated Testing

Create a test file in `tests/`:

```python
import unittest
from driver_manager import DriverManager

class TestMyDriver(unittest.TestCase):
    def setUp(self):
        self.manager = DriverManager("drivers")
        self.manager.load_driver("my_custom_driver")
    
    def test_command(self):
        result = self.manager.execute_command("MyDriver", "my_command", "test")
        self.assertIn("test", str(result))
    
    def tearDown(self):
        self.manager.shutdown_all()
```

## Advanced Features

### Interacting with External Programs

```python
import subprocess

class ExternalAppDriver(DriverInterface):
    def __init__(self):
        super().__init__("ExternalApp", "1.0.0", "Controls external app")
        self.process = None
    
    def initialize(self) -> bool:
        try:
            self.process = subprocess.Popen(
                ['external-program'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            print(f"Failed to start external program: {e}")
            return False
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        if command == "send":
            message = args[0] if args else ""
            self.process.stdin.write(f"{message}\n".encode())
            self.process.stdin.flush()
            return "Message sent"
        return f"Unknown command: {command}"
```

### State Management

```python
class StatefulDriver(DriverInterface):
    def __init__(self):
        super().__init__("Stateful", "1.0.0", "Driver with state")
        self.state = {}
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        if command == "set":
            key, value = args[0].split('=')
            self.state[key] = value
            return f"Set {key} = {value}"
        elif command == "get":
            key = args[0]
            return self.state.get(key, "Not found")
        elif command == "list":
            return str(self.state)
```

### File I/O Operations

```python
class DataDriver(DriverInterface):
    def execute(self, command: str, *args, **kwargs) -> Any:
        if command == "save":
            filename, data = args[0], args[1]
            with open(filename, 'w') as f:
                f.write(data)
            return f"Saved to {filename}"
        elif command == "load":
            filename = args[0]
            with open(filename, 'r') as f:
                return f.read()
```

## Troubleshooting

### Driver Not Loading

1. Check filename ends with `_driver.py`
2. Verify class inherits from `DriverInterface`
3. Check for syntax errors
4. Review console output for error messages

### Commands Not Working

1. Ensure command is listed in `get_commands()`
2. Verify command routing in `execute()` method
3. Check for proper error handling
4. Test command logic separately

### Performance Issues

1. Avoid blocking operations in `execute()`
2. Use background threads for long operations
3. Implement caching when appropriate
4. Profile your code to find bottlenecks

## Examples in Repository

Check these example drivers for reference:

- `calculator_driver.py`: Basic arithmetic operations
- `file_manager_driver.py`: File system operations
- `system_info_driver.py`: System information retrieval
- `template_driver_example.py`: Commented template

## Need Help?

- Review existing drivers in `drivers/` directory
- Check the main README.md for general information
- Examine the `DriverInterface` class documentation
