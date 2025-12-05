# LLM Integration Guide

## Overview

The Desktop Assistant now supports natural language processing using Large Language Models (LLMs). This allows users to interact with the assistant using plain English instead of manually selecting drivers and commands.

## Features

### LLM-Powered Mode
When an LLM is enabled with a valid API key, the assistant:
- Understands natural language requests
- Automatically maps requests to appropriate drivers and commands
- Extracts arguments from the request
- Provides conversational responses
- Handles complex, context-aware queries

### Intelligent Fallback Mode
Even without an LLM API key, the assistant provides:
- Keyword-based request parsing
- Common phrase understanding
- Automatic driver/command mapping
- Basic natural language support

## Supported LLM Providers

### OpenAI (Recommended)
- **Models**: GPT-3.5-turbo, GPT-4, GPT-4-turbo
- **Setup**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Cost**: Pay-per-use (very affordable for desktop use)

### Anthropic
- **Models**: Claude-3, Claude-2
- **Setup**: Get API key from [Anthropic Console](https://console.anthropic.com/)
- **Cost**: Pay-per-use

## Configuration

### Method 1: Environment Variable (Recommended)

```bash
# For OpenAI
export OPENAI_API_KEY="sk-your-api-key-here"

# For Anthropic
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Method 2: Config File

Edit `config.json`:

```json
{
  "llm": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key-here"
  }
}
```

**Available providers**: `"openai"`, `"anthropic"`

**OpenAI models**:
- `"gpt-3.5-turbo"` (fastest, cheapest)
- `"gpt-4"` (most capable)
- `"gpt-4-turbo"` (balance of speed and capability)

**Anthropic models**:
- `"claude-3-5-sonnet-20241022"` (latest)
- `"claude-3-opus-20240229"` (most capable)
- `"claude-3-sonnet-20240229"` (balanced)

### Method 3: Programmatic

```python
from assistant_core import AssistantCore

assistant = AssistantCore()
assistant.config["llm"]["enabled"] = True
assistant.config["llm"]["provider"] = "openai"
assistant.config["llm"]["api_key"] = "your-key"
assistant.llm_handler = LLMHandler(assistant.config)
```

## Installation

### Basic Installation
```bash
pip install -r requirements.txt
```

### With OpenAI Support
```bash
pip install openai
```

### With Anthropic Support
```bash
pip install anthropic
```

### With Both
```bash
pip install openai anthropic
```

## Usage Examples

### In GUI Mode

1. Launch the application: `python main.py`
2. Select "Natural Language" mode (radio button at top)
3. Type your request in plain English
4. Press Execute or press Enter

Example requests:
- "What's 25 times 4?"
- "Show me all the files here"
- "Calculate the result of (10 + 5) * 3"
- "Give me system information"

### In CLI Mode

```bash
python cli_nl_demo.py
```

Then type requests interactively:
```
You: Calculate 100 divided by 4
Assistant: Calculating: 100/4

Result: 100/4 = 25.0

You: List the files in this directory
Assistant: Listing files in current directory.

Result: [file listing...]
```

### Programmatic Usage

```python
from assistant_core import AssistantCore

# Initialize
assistant = AssistantCore()
assistant.start()

# Process natural language
result = assistant.process_natural_language("Calculate 5 + 3")

if result['success']:
    print(f"Result: {result['result']}")
else:
    print(f"Error: {result['response']}")

# Clean up
assistant.stop()
```

## How It Works

### With LLM Enabled

1. **User Input**: "Calculate the sum of 15 and 27"

2. **LLM Processing**: The LLM handler creates a prompt with:
   - Available drivers and their commands
   - The user's request
   - Instructions to parse into structured format

3. **LLM Response**: Returns JSON:
   ```json
   {
     "driver": "Calculator",
     "command": "eval",
     "arguments": "15+27",
     "response": "Calculating the sum of 15 and 27",
     "success": true
   }
   ```

4. **Execution**: The assistant executes `Calculator.eval("15+27")`

5. **Result**: Returns "15+27 = 42"

### Fallback Mode (Without LLM)

1. **User Input**: "Calculate 15 + 27"

2. **Keyword Matching**: Detects "calculate" keyword

3. **Extraction**: Extracts mathematical expression "15 + 27"

4. **Mapping**: Maps to `Calculator.eval()`

5. **Execution**: Executes and returns result

## Advanced Configuration

### Customizing Temperature

Lower temperature = more deterministic, higher = more creative

```json
{
  "llm": {
    "enabled": true,
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.3,
    "max_tokens": 500
  }
}
```

### Using Different Models

Switch models based on your needs:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4"  // More capable but slower and pricier
  }
}
```

## Troubleshooting

### "LLM is not enabled"
- Check that `llm.enabled` is `true` in config.json
- Verify API key is set (environment variable or config file)
- Ensure you've installed the required package (`openai` or `anthropic`)

### "Error initializing LLM client"
- Verify your API key is valid
- Check internet connection
- Ensure the package is installed: `pip list | grep openai`

### "Invalid API key"
- Double-check your API key
- Make sure there are no extra spaces or quotes
- Verify the key is for the correct provider

### Fallback Mode Always Active
- Check if LLM is actually enabled in config
- Verify API key is set correctly
- Look for initialization errors in console output

## Cost Estimation

### OpenAI GPT-3.5-turbo
- Input: ~$0.0015 per 1000 tokens
- Output: ~$0.002 per 1000 tokens
- Typical request: ~200-500 tokens total
- **Cost per request**: ~$0.0005 - $0.001 (less than a penny)

### OpenAI GPT-4
- Input: ~$0.03 per 1000 tokens
- Output: ~$0.06 per 1000 tokens
- **Cost per request**: ~$0.01 - $0.03 (1-3 cents)

### Daily Usage Example
- 100 requests/day with GPT-3.5-turbo: ~$0.05 - $0.10/day
- 100 requests/day with GPT-4: ~$1 - $3/day

## Privacy & Security

### Data Handling
- User requests are sent to the LLM provider's API
- No data is stored permanently by the assistant
- Responses are processed locally

### Best Practices
- Don't include sensitive information in requests
- Use environment variables for API keys (not config file)
- Never commit API keys to version control
- Consider using local models for sensitive use cases

## Future Enhancements

Potential improvements:
- Local LLM support (Ollama, LM Studio)
- Conversation history and context
- Multi-turn dialogues
- Custom LLM fine-tuning
- Voice input/output integration

## Examples

### Calculator Operations
```
User: "What's 234 times 56?"
Assistant: Calculating: 234*56
Result: 234*56 = 13104.0

User: "Calculate (50 + 30) / 4"
Assistant: Calculating: (50+30)/4
Result: (50+30)/4 = 20.0
```

### File Operations
```
User: "List all files in the current folder"
Assistant: Listing files in current directory.
Result: [detailed file listing]

User: "Does README.md exist?"
Assistant: Using FileManager driver, executing exists command.
Result: File 'README.md' exists
```

### System Information
```
User: "What operating system am I running?"
Assistant: Gathering system information.
Result: Operating System: Linux 6.11.0-1018-azure

User: "Tell me about the system"
Assistant: Gathering system information.
Result: [complete system information]
```

## Contributing

To add support for a new LLM provider:

1. Update `llm_handler.py`:
   - Add provider initialization in `_initialize_client()`
   - Implement query method (e.g., `_query_newprovider()`)
   - Update `parse_natural_language()` to handle new provider

2. Update documentation

3. Test thoroughly with the new provider

4. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review error messages in console output
