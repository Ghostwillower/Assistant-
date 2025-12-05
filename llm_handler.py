"""
LLM Handler

Handles natural language processing using Large Language Models.
Supports multiple LLM providers (OpenAI, Anthropic, local models).
"""

import json
import os
from typing import Dict, Any, Optional, List
import re


class LLMHandler:
    """
    Handles natural language processing using LLMs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM handler.
        
        Args:
            config: Configuration dictionary with LLM settings
        """
        self.config = config
        self.llm_config = config.get("llm", {})
        self.provider = self.llm_config.get("provider", "openai")
        self.model = self.llm_config.get("model", "gpt-3.5-turbo")
        self.api_key = self.llm_config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.enabled = self.llm_config.get("enabled", False)
        
        # Initialize provider-specific client
        self.client = None
        if self.enabled and self.api_key:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on provider."""
        try:
            if self.provider == "openai":
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=self.api_key)
                    print(f"LLM Handler initialized with OpenAI ({self.model})")
                except ImportError:
                    print("Warning: openai package not installed. Install with: pip install openai")
                    self.enabled = False
            elif self.provider == "anthropic":
                try:
                    import anthropic
                    self.client = anthropic.Anthropic(api_key=self.api_key)
                    print(f"LLM Handler initialized with Anthropic ({self.model})")
                except ImportError:
                    print("Warning: anthropic package not installed. Install with: pip install anthropic")
                    self.enabled = False
            else:
                print(f"Unsupported LLM provider: {self.provider}")
                self.enabled = False
        except Exception as e:
            print(f"Error initializing LLM client: {str(e)}")
            self.enabled = False
    
    def parse_natural_language(self, user_input: str, available_drivers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse natural language input to determine driver and command.
        
        Args:
            user_input: Natural language input from user
            available_drivers: Dictionary of available drivers and their commands
            
        Returns:
            Dict with 'driver', 'command', 'arguments', and 'response' keys
        """
        if not self.enabled or not self.client:
            return self._fallback_parse(user_input, available_drivers)
        
        try:
            # Create context about available drivers and commands
            context = self._build_context(available_drivers)
            
            # Create prompt for LLM
            prompt = self._create_parsing_prompt(user_input, context)
            
            # Get response from LLM
            if self.provider == "openai":
                response = self._query_openai(prompt)
            elif self.provider == "anthropic":
                response = self._query_anthropic(prompt)
            else:
                return self._fallback_parse(user_input, available_drivers)
            
            # Parse the LLM response
            return self._parse_llm_response(response)
            
        except Exception as e:
            print(f"Error in LLM parsing: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": f"Error processing request: {str(e)}"
            }
    
    def _build_context(self, available_drivers: Dict[str, Any]) -> str:
        """Build context string about available drivers and commands."""
        context_parts = ["Available drivers and commands:"]
        
        for driver_name, driver_info in available_drivers.items():
            context_parts.append(f"\nDriver: {driver_name}")
            context_parts.append(f"Description: {driver_info.get('description', 'N/A')}")
            
            commands = driver_info.get('commands', {})
            if commands:
                context_parts.append("Commands:")
                for cmd, desc in commands.items():
                    context_parts.append(f"  - {cmd}: {desc}")
        
        return "\n".join(context_parts)
    
    def _create_parsing_prompt(self, user_input: str, context: str) -> str:
        """Create prompt for LLM to parse user input."""
        return f"""You are an intelligent assistant parser. Your task is to analyze user requests and map them to available system drivers and commands.

{context}

User request: "{user_input}"

Analyze the user's request and respond with a JSON object containing:
- "driver": the name of the driver to use (or null if none match)
- "command": the command to execute (or null if none match)
- "arguments": the argument(s) to pass to the command (or empty string if none)
- "response": a friendly response explaining what you're doing
- "success": true if you can map this to a driver/command, false otherwise

If you cannot map the request to any available driver/command, set success to false and provide a helpful response explaining what's available.

Respond ONLY with the JSON object, no additional text.
"""
    
    def _query_openai(self, prompt: str) -> str:
        """Query OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that parses user requests into structured commands."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    def _query_anthropic(self, prompt: str) -> str:
        """Query Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse the JSON response from LLM."""
        try:
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
                return parsed
            else:
                return {
                    "success": False,
                    "error": "Invalid response format",
                    "response": "Sorry, I couldn't understand that request."
                }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON parsing error: {str(e)}",
                "response": "Sorry, I had trouble processing that request."
            }
    
    def _fallback_parse(self, user_input: str, available_drivers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback parser using simple keyword matching when LLM is not available.
        
        Args:
            user_input: User input string
            available_drivers: Dictionary of available drivers
            
        Returns:
            Dict with parsing results
        """
        user_input_lower = user_input.lower()
        
        # Try to match keywords to drivers
        for driver_name, driver_info in available_drivers.items():
            driver_name_lower = driver_name.lower()
            
            # Check if driver name is mentioned
            if driver_name_lower in user_input_lower:
                commands = driver_info.get('commands', {})
                
                # Try to match a command
                for cmd, desc in commands.items():
                    if cmd.lower() in user_input_lower:
                        # Extract potential arguments (everything after the command)
                        arg_match = re.search(rf'{cmd}\s+(.+)', user_input_lower)
                        arguments = arg_match.group(1) if arg_match else ""
                        
                        return {
                            "success": True,
                            "driver": driver_name,
                            "command": cmd,
                            "arguments": arguments,
                            "response": f"Using {driver_name} driver, executing {cmd} command."
                        }
        
        # Keyword-based matching for common operations
        if any(word in user_input_lower for word in ['calculate', 'add', 'subtract', 'multiply', 'divide', 'math', 'what is']):
            # Extract mathematical expression more carefully
            # Remove common question words
            math_input = user_input_lower
            for word in ['calculate', 'what is', 'compute', 'solve']:
                math_input = math_input.replace(word, '')
            
            # Replace word operators with symbols
            math_input = math_input.replace(' plus ', '+')
            math_input = math_input.replace(' add ', '+')
            math_input = math_input.replace(' minus ', '-')
            math_input = math_input.replace(' subtract ', '-')
            math_input = math_input.replace(' times ', '*')
            math_input = math_input.replace(' multiply by ', '*')
            math_input = math_input.replace(' multiplied by ', '*')
            math_input = math_input.replace(' divided by ', '/')
            math_input = math_input.replace(' by ', '*')
            math_input = math_input.replace('?', '')
            
            # Clean up and extract numbers and operators
            math_expr = re.sub(r'[^0-9+\-*/().\s]', '', math_input)
            math_expr = math_expr.strip()
            
            if math_expr:
                return {
                    "success": True,
                    "driver": "Calculator",
                    "command": "eval",
                    "arguments": math_expr,
                    "response": f"Calculating: {math_expr}"
                }
        
        if any(word in user_input_lower for word in ['file', 'list', 'directory', 'folder']):
            if 'list' in user_input_lower or 'show' in user_input_lower:
                return {
                    "success": True,
                    "driver": "FileManager",
                    "command": "list",
                    "arguments": ".",
                    "response": "Listing files in current directory."
                }
        
        if any(word in user_input_lower for word in ['system', 'os', 'platform', 'info']):
            return {
                "success": True,
                "driver": "SystemInfo",
                "command": "all",
                "arguments": "",
                "response": "Gathering system information."
            }
        
        # No match found
        return {
            "success": False,
            "response": f"I couldn't understand that request. Try mentioning a driver (Calculator, FileManager, SystemInfo) and what you'd like to do.",
            "available_drivers": list(available_drivers.keys())
        }
    
    def get_conversational_response(self, user_input: str, context: str = "") -> str:
        """
        Get a conversational response from the LLM.
        
        Args:
            user_input: User's message
            context: Additional context
            
        Returns:
            LLM's response
        """
        if not self.enabled or not self.client:
            return "LLM is not enabled. Please configure an API key."
        
        try:
            prompt = f"{context}\n\nUser: {user_input}\n\nAssistant:" if context else user_input
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful desktop assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            else:
                return "Unsupported LLM provider."
                
        except Exception as e:
            return f"Error getting response: {str(e)}"
