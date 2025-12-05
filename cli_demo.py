"""
CLI Demo - Command Line Interface Demo

Demonstrates the desktop assistant functionality without GUI.
"""

from assistant_core import AssistantCore


def demo():
    """
    Run a demonstration of the assistant's capabilities.
    """
    print("=" * 60)
    print("Desktop Assistant - CLI Demo")
    print("=" * 60)
    
    # Create and start the assistant
    assistant = AssistantCore()
    assistant.start()
    
    print("\n--- Loaded Drivers ---")
    drivers = assistant.get_loaded_drivers()
    for name, info in drivers.items():
        print(f"  {name} v{info['version']}: {info['description']}")
    
    # Demo Calculator Driver
    print("\n" + "=" * 60)
    print("Calculator Driver Demo")
    print("=" * 60)
    
    calc_commands = assistant.get_driver_commands("Calculator")
    print("\nAvailable commands:")
    for cmd, desc in calc_commands.items():
        print(f"  {cmd}: {desc}")
    
    print("\nExamples:")
    examples = [
        ("add", "10+20+30"),
        ("subtract", "100-25"),
        ("multiply", "6*7"),
        ("divide", "100/5"),
        ("eval", "(5+3)*2")
    ]
    
    for cmd, expr in examples:
        result = assistant.execute_command("Calculator", cmd, expr)
        print(f"  {result}")
    
    # Demo File Manager Driver
    print("\n" + "=" * 60)
    print("File Manager Driver Demo")
    print("=" * 60)
    
    fm_commands = assistant.get_driver_commands("FileManager")
    print("\nAvailable commands:")
    for cmd, desc in fm_commands.items():
        print(f"  {cmd}: {desc}")
    
    print("\nExamples:")
    print(f"  {assistant.execute_command('FileManager', 'cwd')}")
    print(f"\n  {assistant.execute_command('FileManager', 'exists', 'README.md')}")
    print(f"\n  Listing current directory:")
    result = assistant.execute_command('FileManager', 'list', '.')
    print("  " + "\n  ".join(result.split("\n")))
    
    # Demo System Info Driver
    print("\n" + "=" * 60)
    print("System Info Driver Demo")
    print("=" * 60)
    
    sys_commands = assistant.get_driver_commands("SystemInfo")
    print("\nAvailable commands:")
    for cmd, desc in sys_commands.items():
        print(f"  {cmd}: {desc}")
    
    print("\nExamples:")
    print(f"  {assistant.execute_command('SystemInfo', 'os')}")
    print(f"  {assistant.execute_command('SystemInfo', 'python')[:80]}...")
    
    # Shutdown
    print("\n" + "=" * 60)
    assistant.stop()
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
