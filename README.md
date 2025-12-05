# Desktop Assistant

A modular desktop assistant application with a plugin-based driver system that allows interaction with external programs and objects.

## Features

- **Modular Architecture**: Import custom drivers/modules to extend functionality
- **Plugin System**: Easy-to-use driver interface for creating new capabilities
- **Desktop GUI**: User-friendly interface built with Tkinter
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
# Clone the repository
git clone https://github.com/Ghostwillower/Assistant-.git
cd Assistant-

# Install dependencies (Python 3.7+)
pip install -r requirements.txt

# Run the assistant
python main.py
```

## Architecture

### Core Components

1. **Assistant Core** (`assistant_core.py`): Main application logic
2. **Driver Manager** (`driver_manager.py`): Handles loading and managing drivers
3. **Driver Interface** (`driver_interface.py`): Base class for all drivers
4. **GUI** (`gui.py`): Desktop interface for user interaction

### Creating Custom Drivers

Drivers are modules that extend the assistant's capabilities. Each driver inherits from `DriverInterface` and implements specific methods:

```python
from driver_interface import DriverInterface

class MyDriver(DriverInterface):
    def __init__(self):
        super().__init__("MyDriver", "1.0", "Description of my driver")
    
    def initialize(self):
        """Called when driver is loaded"""
        pass
    
    def execute(self, command, *args, **kwargs):
        """Execute a command with this driver"""
        pass
    
    def shutdown(self):
        """Called when driver is unloaded"""
        pass
```

## Included Drivers

- **Calculator**: Basic arithmetic operations
- **File Manager**: File system operations (list, read, create)
- **System Info**: Display system information

## Project Structure

```
Assistant-/
├── main.py                    # Application entry point
├── assistant_core.py          # Core assistant logic
├── driver_manager.py          # Driver loading and management
├── driver_interface.py        # Base driver interface
├── gui.py                     # Desktop GUI
├── config.json                # Configuration file
├── drivers/                   # Driver modules directory
│   ├── __init__.py
│   ├── calculator_driver.py
│   ├── file_manager_driver.py
│   └── system_info_driver.py
├── tests/                     # Unit tests
│   └── test_driver_manager.py
└── requirements.txt           # Python dependencies
```

## Usage

1. Launch the application: `python main.py`
2. Use the GUI to interact with available drivers
3. Add custom drivers by placing them in the `drivers/` directory
4. Drivers are automatically discovered and loaded at startup

## License

MIT License
