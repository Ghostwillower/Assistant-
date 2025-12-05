"""
Desktop GUI

Graphical user interface for the desktop assistant.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional
from assistant_core import AssistantCore


class AssistantGUI:
    """
    Desktop GUI for the assistant application.
    """
    
    def __init__(self, assistant: AssistantCore):
        """
        Initialize the GUI.
        
        Args:
            assistant: AssistantCore instance
        """
        self.assistant = assistant
        self.root = tk.Tk()
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """
        Setup the main window.
        """
        config = self.assistant.config.get("window_settings", {})
        self.root.title(config.get("title", "Desktop Assistant"))
        self.root.geometry(f"{config.get('width', 800)}x{config.get('height', 600)}")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_widgets(self):
        """
        Create and layout GUI widgets.
        """
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text=self.assistant.config['app_name'],
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Driver selection frame
        driver_frame = ttk.LabelFrame(main_frame, text="Drivers", padding="5")
        driver_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        driver_frame.columnconfigure(1, weight=1)
        
        # Driver dropdown
        ttk.Label(driver_frame, text="Select Driver:").grid(row=0, column=0, padx=(0, 5))
        self.driver_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(driver_frame, textvariable=self.driver_var, state='readonly')
        self.driver_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.driver_combo.bind('<<ComboboxSelected>>', self._on_driver_selected)
        
        # Refresh button
        ttk.Button(driver_frame, text="Refresh", command=self._refresh_drivers).grid(row=0, column=2)
        
        # Command selection frame
        command_frame = ttk.LabelFrame(main_frame, text="Commands", padding="5")
        command_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        command_frame.columnconfigure(0, weight=1)
        command_frame.rowconfigure(0, weight=1)
        
        # Command list
        self.command_list = tk.Listbox(command_frame, height=6)
        self.command_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.command_list.bind('<<ListboxSelect>>', self._on_command_selected)
        
        # Command scrollbar
        command_scroll = ttk.Scrollbar(command_frame, orient=tk.VERTICAL, command=self.command_list.yview)
        command_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.command_list.configure(yscrollcommand=command_scroll.set)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="5")
        input_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(input_frame, text="Execute", command=self._execute_command).grid(row=0, column=1)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=2)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, state='disabled')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize with loaded drivers
        self._refresh_drivers()
        self._log_output("Assistant started. Select a driver to begin.")
    
    def _refresh_drivers(self):
        """
        Refresh the list of available drivers.
        """
        drivers = self.assistant.get_loaded_drivers()
        driver_names = list(drivers.keys())
        self.driver_combo['values'] = driver_names
        
        if driver_names and not self.driver_var.get():
            self.driver_combo.current(0)
            self._on_driver_selected()
        
        self._log_output(f"Loaded {len(driver_names)} driver(s)")
    
    def _on_driver_selected(self, event=None):
        """
        Handle driver selection.
        """
        driver_name = self.driver_var.get()
        if driver_name:
            commands = self.assistant.get_driver_commands(driver_name)
            self.command_list.delete(0, tk.END)
            
            if commands:
                for cmd, desc in commands.items():
                    self.command_list.insert(tk.END, f"{cmd}: {desc}")
                self._log_output(f"Selected driver: {driver_name}")
    
    def _on_command_selected(self, event=None):
        """
        Handle command selection.
        """
        selection = self.command_list.curselection()
        if selection:
            command_text = self.command_list.get(selection[0])
            command = command_text.split(':')[0].strip()
            self._log_output(f"Selected command: {command}")
    
    def _execute_command(self):
        """
        Execute the selected command with input.
        """
        driver_name = self.driver_var.get()
        selection = self.command_list.curselection()
        
        if not driver_name:
            messagebox.showwarning("No Driver", "Please select a driver first.")
            return
        
        if not selection:
            messagebox.showwarning("No Command", "Please select a command first.")
            return
        
        command_text = self.command_list.get(selection[0])
        command = command_text.split(':')[0].strip()
        input_value = self.input_entry.get()
        
        self._log_output(f"\n> Executing: {driver_name}.{command}({input_value})")
        
        try:
            result = self.assistant.execute_command(driver_name, command, input_value)
            self._log_output(f"Result: {result}")
        except Exception as e:
            self._log_output(f"Error: {str(e)}")
        
        self.input_entry.delete(0, tk.END)
    
    def _log_output(self, message: str):
        """
        Log a message to the output area.
        
        Args:
            message: Message to log
        """
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state='disabled')
    
    def _on_close(self):
        """
        Handle window close event.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit the assistant?"):
            self.assistant.stop()
            self.root.destroy()
    
    def run(self):
        """
        Start the GUI main loop.
        """
        self.root.mainloop()
