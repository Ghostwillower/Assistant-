"""
CLI Natural Language Demo

Demonstrates the desktop assistant's natural language capabilities.
"""

from assistant_core import AssistantCore


def demo():
    """
    Run a demonstration of the assistant's natural language capabilities.
    """
    print("=" * 60)
    print("Desktop Assistant - Natural Language Demo")
    print("=" * 60)
    
    # Create and start the assistant
    assistant = AssistantCore()
    assistant.start()
    
    print("\n--- System Status ---")
    print(f"LLM Enabled: {assistant.is_llm_enabled()}")
    
    if not assistant.is_llm_enabled():
        print("\nNote: LLM is not enabled. The assistant will use fallback")
        print("keyword matching. To enable LLM, configure API key in config.json")
        print("or set OPENAI_API_KEY environment variable.")
    
    print("\n--- Loaded Drivers ---")
    drivers = assistant.get_loaded_drivers()
    for name, info in drivers.items():
        print(f"  {name} v{info['version']}: {info['description']}")
    
    # Demo natural language requests
    print("\n" + "=" * 60)
    print("Natural Language Request Examples")
    print("=" * 60)
    
    examples = [
        "Calculate 15 + 27",
        "What is 100 divided by 5?",
        "Show me the files in the current directory",
        "Tell me about the system",
        "Multiply 6 by 8",
    ]
    
    for i, request in enumerate(examples, 1):
        print(f"\n{i}. Request: \"{request}\"")
        print("-" * 60)
        
        result = assistant.process_natural_language(request)
        
        if result.get('success'):
            print(f"✓ Understood!")
            print(f"  Driver: {result.get('driver')}")
            print(f"  Command: {result.get('command')}")
            if result.get('arguments'):
                print(f"  Arguments: {result.get('arguments')}")
            print(f"\n  Response: {result.get('response', 'N/A')}")
            if result.get('result'):
                print(f"  Result: {result.get('result')}")
        else:
            print(f"✗ Could not understand")
            print(f"  Response: {result.get('response', 'N/A')}")
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode")
    print("=" * 60)
    print("Type your requests in natural language (or 'quit' to exit)")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            result = assistant.process_natural_language(user_input)
            
            if result.get('success'):
                print(f"Assistant: {result.get('full_response', result.get('response', 'Done!'))}")
            else:
                print(f"Assistant: {result.get('response', 'I could not process that.')}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            break
    
    # Shutdown
    print("\n" + "=" * 60)
    assistant.stop()
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
