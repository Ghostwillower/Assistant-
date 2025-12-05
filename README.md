# Desktop Assistant

A modular desktop assistant application with a plugin-based driver system and **natural language processing** capabilities using Large Language Models (LLMs).

## Features

- **Natural Language Interface**: Ask questions in plain English using LLM integration
- **Modular Architecture**: Import custom drivers/modules to extend functionality
- **Plugin System**: Easy-to-use driver interface for creating new capabilities
- **Desktop GUI**: User-friendly interface built with Tkinter
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Intelligent Fallback**: Works with or without LLM API keys using keyword matching

## Installation

```bash
# Clone the repository
git clone https://github.com/Ghostwillower/Assistant-.git
cd Assistant-

# Install dependencies (Python 3.7+)
pip install -r requirements.txt

# Optional: Install LLM support for natural language processing
pip install openai  # For OpenAI GPT models
# OR
pip install anthropic  # For Anthropic Claude models

# Run the assistant
python main.py
```

## Natural Language Mode

The assistant now supports natural language input! You can interact with it using plain English instead of manually selecting drivers and commands.

### Enabling LLM

1. **Using OpenAI** (recommended):
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - Set environment variable: `export OPENAI_API_KEY="your-key-here"`
   - Or edit `config.json` and set `llm.api_key`

2. **Using Anthropic**:
   - Get an API key from [Anthropic](https://console.anthropic.com/)
   - Edit `config.json`: set `llm.provider` to `"anthropic"` and add your API key

3. **Enable in config.json**:
   ```json
   "llm": {
     "enabled": true,
     "provider": "openai",
     "model": "gpt-3.5-turbo",
     "api_key": "your-api-key-here"
   }
   ```

### Example Natural Language Requests

- "Calculate 15 + 27"
- "What is 100 divided by 5?"
- "Show me the files in the current directory"
- "Tell me about the system"
- "Multiply 6 by 8"

### Fallback Mode

Even without an LLM API key, the assistant uses intelligent keyword matching to understand common requests!

## Architecture

### Core Components

1. **Assistant Core** (`assistant_core.py`): Main application logic with LLM integration
2. **LLM Handler** (`llm_handler.py`): Natural language processing using LLMs
3. **Driver Manager** (`driver_manager.py`): Handles loading and managing drivers
4. **Driver Interface** (`driver_interface.py`): Base class for all drivers
5. **GUI** (`gui.py`): Desktop interface with natural language and driver modes

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

## Usage

### GUI Mode

1. Launch the application: `python main.py`
2. Choose between **Natural Language** or **Driver Mode**:
   - **Natural Language Mode**: Type requests in plain English
   - **Driver Mode**: Select a driver and command manually
3. Enter your request or input and press Execute (or press Enter)

### CLI Demo

Run the classic driver demo:
```bash
python cli_demo.py
```

Run the natural language demo:
```bash
python cli_nl_demo.py
```

### Using Natural Language

In the GUI, switch to "Natural Language" mode and type requests like:
- "Calculate the sum of 45 and 67"
- "List all files in the current folder"
- "What operating system am I using?"

The assistant will automatically:
1. Parse your request using LLM (or keyword matching)
2. Determine the appropriate driver and command
3. Execute the command with the right arguments
4. Display the results

## Project Structure

```
Assistant-/
├── main.py                    # Application entry point
├── assistant_core.py          # Core assistant logic with LLM integration
├── llm_handler.py             # LLM natural language processing
├── driver_manager.py          # Driver loading and management
├── driver_interface.py        # Base driver interface
├── gui.py                     # Desktop GUI with NL support
├── cli_demo.py                # Classic CLI demo
├── cli_nl_demo.py             # Natural language CLI demo
├── config.json                # Configuration file (with LLM settings)
├── drivers/                   # Driver modules directory
│   ├── __init__.py
│   ├── calculator_driver.py
│   ├── file_manager_driver.py
│   └── system_info_driver.py
├── tests/                     # Unit tests
│   ├── test_driver_manager.py
│   └── test_llm_handler.py
└── requirements.txt           # Python dependencies
```

## License

MIT License
