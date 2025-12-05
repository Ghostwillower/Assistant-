"""
Desktop Assistant - Main Entry Point

A modular desktop assistant with plugin-based driver system.
"""

from assistant_core import AssistantCore
from gui import AssistantGUI


def main():
    """
    Main application entry point.
    """
    # Create and start the assistant core
    assistant = AssistantCore()
    assistant.start()
    
    # Create and run the GUI
    gui = AssistantGUI(assistant)
    gui.run()


if __name__ == "__main__":
    main()
