#!/usr/bin/env python
import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class ScriptRunnerApp:
    def __init__(self):
        self.window = Gtk.Window(title="Script Runner")
        self.window.set_default_size(400, 300)
        self.window.connect("destroy", Gtk.main_quit)

        # Create a vertical box to hold buttons and output
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(self.box)

        # Get a list of Python files in the current directory
        self.python_files = [f for f in os.listdir('.') if f.lower().endswith('.py')]
        self.python_files.sort()

        # Create buttons for each Python script
        for filename in self.python_files:
            if filename == "menu.py":
                continue
            display_name = filename.replace('_', ' ').replace('.py','').title()
            button = Gtk.Button(label=display_name)
            button.connect("clicked", self.run_script, filename)
            self.box.pack_start(button, False, False, 0)

        # exit button
        button = Gtk.Button(label="Exit")
        button.connect("clicked", exit)
        self.box.pack_start(button, False, False, 0)

        # Create a scrolled window for output
        self.scrolled_window = Gtk.ScrolledWindow()
        self.text_view = Gtk.TextView()
        self.text_view.set_size_request(260, 300)
        self.text_buffer = self.text_view.get_buffer()
        self.scrolled_window.add(self.text_view)
        self.box.pack_start(self.scrolled_window, True, True, 0)

        self.window.show_all()

    def run_script(self, button, filename):
        try:
            output = subprocess.check_output(['python', filename], stderr=subprocess.STDOUT, text=True)
            self.text_buffer.insert_at_cursor(f"Output from {filename}:\n{output}\n\n")
        except subprocess.CalledProcessError as e:
            self.text_buffer.insert_at_cursor(f"Error executing {filename}:\n{e.output}\n\n")

if __name__ == "__main__":
    app = ScriptRunnerApp()
    Gtk.main()

