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
        main_frame.rowconfigure(3, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text=self.assistant.config['app_name'],
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Mode selection (Natural Language vs Driver Mode)
        mode_frame = ttk.LabelFrame(main_frame, text="Input Mode", padding="5")
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.mode_var = tk.StringVar(value="natural" if self.assistant.is_llm_enabled() else "driver")
        ttk.Radiobutton(mode_frame, text="Natural Language", variable=self.mode_var, 
                       value="natural", command=self._on_mode_change).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="Driver Mode", variable=self.mode_var, 
                       value="driver", command=self._on_mode_change).grid(row=0, column=1, padx=5)
        
        # LLM status indicator
        llm_status = "🟢 LLM Enabled" if self.assistant.is_llm_enabled() else "🔴 LLM Disabled"
        self.llm_status_label = ttk.Label(mode_frame, text=llm_status)
        self.llm_status_label.grid(row=0, column=2, padx=20)
        
        # Driver selection frame (visible in driver mode)
        self.driver_frame = ttk.LabelFrame(main_frame, text="Drivers", padding="5")
        self.driver_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.driver_frame.columnconfigure(1, weight=1)
        
        # Driver dropdown
        ttk.Label(self.driver_frame, text="Select Driver:").grid(row=0, column=0, padx=(0, 5))
        self.driver_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(self.driver_frame, textvariable=self.driver_var, state='readonly')
        self.driver_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.driver_combo.bind('<<ComboboxSelected>>', self._on_driver_selected)
        
        # Refresh button
        ttk.Button(self.driver_frame, text="Refresh", command=self._refresh_drivers).grid(row=0, column=2)
        
        # Command selection frame (visible in driver mode)
        self.command_frame = ttk.LabelFrame(main_frame, text="Commands", padding="5")
        self.command_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.command_frame.columnconfigure(0, weight=1)
        self.command_frame.rowconfigure(0, weight=1)
        
        # Command list
        self.command_list = tk.Listbox(self.command_frame, height=6)
        self.command_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.command_list.bind('<<ListboxSelect>>', self._on_command_selected)
        
        # Command scrollbar
        command_scroll = ttk.Scrollbar(self.command_frame, orient=tk.VERTICAL, command=self.command_list.yview)
        command_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.command_list.configure(yscrollcommand=command_scroll.set)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="5")
        input_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.input_entry.bind('<Return>', lambda e: self._execute_command())
        
        ttk.Button(input_frame, text="Execute", command=self._execute_command).grid(row=0, column=1)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        output_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=2)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, state='disabled')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize with loaded drivers
        self._refresh_drivers()
        self._on_mode_change()
        
        welcome_msg = "Assistant started."
        if self.assistant.is_llm_enabled():
            welcome_msg += " Natural language mode is available. Try asking questions!"
        else:
            welcome_msg += " Select a driver to begin, or enable LLM in config.json for natural language."
        self._log_output(welcome_msg)
    
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
    
    def _on_mode_change(self):
        """
        Handle input mode change.
        """
        mode = self.mode_var.get()
        
        if mode == "natural":
            # Hide driver and command selection in natural language mode
            self.driver_frame.grid_remove()
            self.command_frame.grid_remove()
            self._log_output("Switched to Natural Language mode. Type your request in plain English!")
        else:
            # Show driver and command selection in driver mode
            self.driver_frame.grid()
            self.command_frame.grid()
            self._log_output("Switched to Driver mode. Select a driver and command.")
    
    def _execute_command(self):
        """
        Execute the selected command with input.
        """
        input_value = self.input_entry.get()
        
        if not input_value:
            messagebox.showwarning("No Input", "Please enter some input.")
            return
        
        mode = self.mode_var.get()
        
        if mode == "natural":
            # Natural language mode
            self._log_output(f"\n> {input_value}")
            
            try:
                result = self.assistant.process_natural_language(input_value)
                
                if result.get('success'):
                    response = result.get('full_response') or result.get('response', 'Done!')
                    self._log_output(response)
                else:
                    response = result.get('response', 'Sorry, I could not process that request.')
                    self._log_output(response)
            except Exception as e:
                self._log_output(f"Error: {str(e)}")
        else:
            # Driver mode
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
