"""
Unit tests for the LLM Handler and Natural Language Processing
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_handler import LLMHandler
from assistant_core import AssistantCore


class TestLLMHandler(unittest.TestCase):
    """Test cases for LLMHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create config without LLM enabled (uses fallback)
        self.config = {
            "llm": {
                "enabled": False,
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "api_key": ""
            }
        }
        self.handler = LLMHandler(self.config)
        
        # Sample available drivers for testing
        self.available_drivers = {
            "Calculator": {
                "description": "Basic arithmetic calculator",
                "commands": {
                    "add": "Add numbers",
                    "eval": "Evaluate expression"
                }
            },
            "FileManager": {
                "description": "File system operations",
                "commands": {
                    "list": "List files",
                    "read": "Read file"
                }
            }
        }
    
    def test_llm_handler_initialization(self):
        """Test LLM handler initialization"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.provider, "openai")
        self.assertFalse(self.handler.enabled)
    
    def test_fallback_parse_calculator(self):
        """Test fallback parser with calculator requests"""
        test_cases = [
            ("Calculate 5 + 3", "Calculator", "eval"),
            ("What is 10 times 2?", "Calculator", "eval"),
            ("Multiply 6 by 8", "Calculator", "eval"),
            ("100 divided by 5", "Calculator", "eval"),
        ]
        
        for user_input, expected_driver, expected_command in test_cases:
            result = self.handler.parse_natural_language(user_input, self.available_drivers)
            self.assertTrue(result.get('success'), f"Failed to parse: {user_input}")
            self.assertEqual(result.get('driver'), expected_driver)
            self.assertEqual(result.get('command'), expected_command)
    
    def test_fallback_parse_file_manager(self):
        """Test fallback parser with file manager requests"""
        test_cases = [
            "Show me the files",
            "List directory",
            "Show files in current folder"
        ]
        
        for user_input in test_cases:
            result = self.handler.parse_natural_language(user_input, self.available_drivers)
            self.assertTrue(result.get('success'), f"Failed to parse: {user_input}")
            self.assertEqual(result.get('driver'), "FileManager")
            self.assertEqual(result.get('command'), "list")
    
    def test_fallback_parse_unknown_request(self):
        """Test fallback parser with unknown requests"""
        result = self.handler.parse_natural_language(
            "Play some music", 
            self.available_drivers
        )
        self.assertFalse(result.get('success'))
        self.assertIn('response', result)
    
    def test_build_context(self):
        """Test building context from available drivers"""
        context = self.handler._build_context(self.available_drivers)
        self.assertIn("Calculator", context)
        self.assertIn("FileManager", context)
        self.assertIn("eval", context)
        self.assertIn("list", context)


class TestAssistantNaturalLanguage(unittest.TestCase):
    """Test cases for Assistant Core natural language processing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = AssistantCore()
        self.assistant.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.assistant.stop()
    
    def test_process_natural_language_calculator(self):
        """Test natural language processing with calculator"""
        result = self.assistant.process_natural_language("Calculate 5 + 3")
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('driver'), "Calculator")
    
    def test_process_natural_language_file_manager(self):
        """Test natural language processing with file manager"""
        result = self.assistant.process_natural_language("List files")
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('driver'), "FileManager")
    
    def test_is_llm_enabled(self):
        """Test checking if LLM is enabled"""
        enabled = self.assistant.is_llm_enabled()
        self.assertIsInstance(enabled, bool)
    
    def test_process_natural_language_returns_result(self):
        """Test that natural language processing returns actual results"""
        result = self.assistant.process_natural_language("Show system info")
        # Should either succeed or return a helpful message
        self.assertIn('response', result)


if __name__ == '__main__':
    unittest.main()
