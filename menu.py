#!/usr/bin/env python
import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
from hcloud import Client

class ScriptRunnerApp:
    def __init__(self):

        self.window = Gtk.Window(title="Script Runner")
        self.window.set_default_size(600, 400)
        self.window.connect("destroy", Gtk.main_quit)

        # Create a grid to organize the layout
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_border_width(10)
        self.window.add(grid)

        # 
        # Widgets for the left side
        # 

        # Get a list of Python files in the current directory
        self.python_files = [f for f in os.listdir('.') if f.lower().endswith('.py')]
        self.python_files.sort()

        # Create buttons for each Python script
        i = 0
        for filename in self.python_files:
            if filename == "menu.py":
                continue
            display_name = filename.replace('_', ' ').replace('.py','').title()
            button = Gtk.Button(label=display_name)
            button.connect("clicked", self.run_script, filename)
            grid.attach(button, 0, i, 1, 1)
            i += 1

        # Create a grid to organize the layout of the spinner and its label
        spinner_grid = Gtk.Grid()
        spinner_grid.set_column_homogeneous(True)
        spinner_grid.set_row_homogeneous(True)
        spinner_grid.set_border_width(10)

        # Create a label for the spinner
        spinner_label = Gtk.Label(label="Servers:")
        spinner_grid.attach(spinner_label, 0, 0, 1, 1)

        # Create a spinner with default value 5
        adjustment = Gtk.Adjustment(
            value=5, lower=1, upper=10, step_increment=1, page_increment=1, page_size=0)
        self.spin_box = Gtk.SpinButton(adjustment=adjustment)
        self.spin_box.set_numeric(True)
        spinner_grid.attach(self.spin_box, 1, 0, 1, 1)
        # Drop the spinner grid into the parent grid
        grid.attach(spinner_grid, 0, i, 1, 1)

        # Retrieve the API token from an environment variable
        api_token = os.environ.get("HETZNER_API_TOKEN")

        if not api_token:
            print("Please set the HETZNER_API_TOKEN environment variable.")
            exit(1)

        # Initialize the client with the API token
        client = Client(token=api_token)
        # Fetch server types
        server_types = client.server_types.get_all()

        # Create a combobox
        self.combobox = Gtk.ComboBoxText()
        for server_type in server_types:
            self.combobox.append_text(server_type.name)
        self.combobox.set_active(0)
        # Add the combobox to the window
        i += 1
        grid.attach(self.combobox, 0, i, 1, 1)

        # 
        # Widgets for the right side
        # 

        # Create a scrolled text view in the right-hand area
        scrolled_window = Gtk.ScrolledWindow()
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_buffer = text_view.get_buffer()
        scrolled_window.add(text_view)
        # i for how many rows to fill with the widget
        # -1 to leave space for exit button
        grid.attach(scrolled_window, 1, 0, 1, i-1)


        # exit button
        exit_button = Gtk.Button(label="Exit")
        exit_button.connect("clicked", self.on_window_destroy)
        grid.attach(exit_button, 1, i, 1, 1)

        # Load the last used value (if any)
        self.load_last_value()
        self.window.connect("destroy", self.on_window_destroy)
        self.window.show_all()

    def run_script(self, button, filename):
        try:
            count = int(self.spin_box.get_value())
            server_type = str(
                self.combobox.get_model()[self.combobox.get_active()][0])
            output = subprocess.check_output(['python', filename, str(count), server_type], stderr=subprocess.STDOUT, text=True)
            self.text_buffer.set_text("")
            self.text_buffer.insert_at_cursor(f"Output from {filename}:\n{output}\n\n")
        except subprocess.CalledProcessError as e:
            self.text_buffer.insert_at_cursor(f"Error executing {filename}:\n{e.output}\n\n")

    def on_window_destroy(self, widget):
        # Save the current value when the window is closed
        self.save_last_value()
        Gtk.main_quit()

    def load_last_value(self):
        try:
            with open("server_count.txt", "r") as file:
                last_value = int(file.read())
                self.spin_box.set_value(last_value)
        except FileNotFoundError:
            pass

    def save_last_value(self):
        last_value = int(self.spin_box.get_value())
        with open("server_count.txt", "w") as file:
            file.write(str(last_value))

if __name__ == "__main__":
    app = ScriptRunnerApp()
    Gtk.main()
