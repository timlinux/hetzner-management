#!/usr/bin/env python
import os
import subprocess
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gio", "2.0")
gi.require_version(namespace="Adw", version="1")
from gi.repository import Gtk, GLib, Gdk, Gio, Adw

from hcloud import Client
import keyring


class HetznerManagement(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Retrieve the API token from an environment variable
        self.api_key = None

        self.set_default_size(600, 250)
        self.set_title("Hetzner Management App")        
        
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        # Create a new "Action"
        action = Gio.SimpleAction.new("something", None)
        action.connect("activate", self.print_something)
        self.add_action(action)  # Here the action is being added to the window, but you could add it to the
                                 # application or an "ActionGroup"

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append("Do Something", "win.something")  # Or you would do app.something if you had attached the
                                                      # action to the application

        # Create a popover
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon

        # Add menu button to the header bar
        self.header.pack_start(self.hamburger)

        
        if os.environ.get("HETZNER_API_TOKEN"):
            self.api_key = os.environ.get("HETZNER_API_TOKEN")

        # otherwise get from the keystore
        if not self.api_key:
            self.api_key = keyring.get_password("HetznerManagementApp", "api_key")

        #
        # Set up the settings dialog for storing the api key etc.
        #
        # self.create_settings_dialog(self)

        if not self.api_key:
            print("Please set the HETZNER_API_TOKEN environment variable.")
            # self.settings.run_dispose()
            exit(1)

        #
        # Now the main dialog content
        #

        # Create a box to organize the layout
        self.parent_box = Gtk.Box()
        self.parent_box.set_direction(dir=Gtk.Orientation.HORIZONTAL)
        self.set_child(self.parent_box)
        #
        # Widgets for the left side
        #
        self.left_column_box = Gtk.Box()
        self.left_column_box.set_direction(dir=Gtk.Orientation.VERTICAL)
        self.left_column_box.set_spacing(10)
        self.left_column_box.set_margin_top(10)
        self.left_column_box.set_margin_bottom(10)
        self.left_column_box.set_margin_start(10)
        self.left_column_box.set_margin_end(10)        


        # Create buttons for each Python script
        buttons = self.make_script_buttons()
        for button in buttons:
            self.left_column_box.append(button)
        # Create a grid to organize the layout of the spinner and its label
        self.spinner_box = Gtk.Box()
        self.spinner_box.set_direction(dir=Gtk.Orientation.HORIZONTAL)

        # Create a label for the spinner
        self.spinner_label = Gtk.Label(label="Servers:")
        self.spinner_box.append(self.spinner_label)

        # Create a spinner with default value 5
        adjustment = Gtk.Adjustment(
            value=5, lower=1, upper=10, step_increment=1, page_increment=1, page_size=0
        )
        self.server_count_spinner = Gtk.SpinButton(adjustment=adjustment)
        self.server_count_spinner.set_numeric(True)
        self.spinner_box.append(self.server_count_spinner)
        # Drop the spinner grid into the box
        self.left_column_box.append(self.spinner_box)

        # Add the combobox to the box
        self.combo = self.create_server_types_combo()
        self.left_column_box.append(self.combo)

        #
        # Widgets for the right side
        #
        self.right_column_box = Gtk.Box()
        self.right_column_box.set_direction(dir=Gtk.Orientation.VERTICAL)
        self.right_column_box.set_spacing(10)
        self.right_column_box.set_margin_top(10)
        self.right_column_box.set_margin_bottom(10)
        self.right_column_box.set_margin_start(10)
        self.right_column_box.set_margin_end(10) 
        # Create a scrolled text view in the right-hand area
        scrolled_window = Gtk.ScrolledWindow()
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_buffer = text_view.get_buffer()
        scrolled_window.set_child(text_view)
        self.left_column_box.append(scrolled_window)

        # exit button
        exit_button = Gtk.Button(label="Exit")
        exit_button.connect("clicked", self.on_window_destroy)
        self.right_column_box.append(exit_button)


    def print_something(self, action, param):
        print("Something!")

    def make_script_buttons(self):
        # Get a list of Python files in the current directory
        python_files = [f for f in os.listdir(".") if f.lower().endswith(".py")]
        python_files.sort()        
        buttons = []
        for filename in python_files:
            if filename == "menu.py":
                continue
            # if filename[0] not in [0,1,2,3,4,5,6,7,8,9]:
            #    continue
            display_name = filename.replace("_", " ").replace(".py", "").title()
            button = Gtk.Button(label=display_name)
            button.connect("clicked", self.run_script, filename)
            buttons.append(button)
        return buttons

    def create_server_types_combo(self):
        client = Client(token=self.api_key)
        server_types = client.server_types.get_all()        
        first_id = None
        combo = Gtk.ComboBoxText()
        for server_type in server_types:
            combo.append(id=server_type.name,text=server_type.name)
            if not first_id:
                first_id = server_type.name
        combo.set_active_id(first_id)
        return combo

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            self.settings.set_string(
                "server-prefix", self.server_prefix_entry.get_text()
            )
            keyring.set_password(
                "ServerSettingsApp", "api_key", self.api_key_entry.get_text()
            )

        # Load the last used value (if any)
        self.load_last_value()
        dialog.connect("destroy", self.on_window_destroy)
        dialog.show_all()
        dialog.present()

    def create_settings_dialog(self, win):
        self.settings = Gio.Settings.new()
        # Create a settings dialog
        self.settings_dialog = Gtk.Dialog(parent=win)
        self.settings_dialog.set_transient_for(win)
        box = self.settings_dialog.get_content_area()
        # Create widgets for API key and server name prefix
        self.api_key_entry = Gtk.Entry()
        self.api_key_entry.set_text(self.api_key)
        self.server_prefix_entry = Gtk.Entry()
        self.server_prefix_entry.set_text(self.settings.get_string("server-prefix"))

        settings_grid = Gtk.Grid()
        settings_grid.set_column_homogeneous(True)
        settings_grid.set_row_homogeneous(True)
        box.add(settings_grid)
        # Add widgets to the dialog
        settings_grid.attach(self.api_key_entry, 0, 0, 1, 1)
        settings_grid.attach(self.server_prefix_entry, 1, 0, 1, 1)
        # Save settings when OK is clicked
        self.settings_dialog.connect("response", self.on_response)

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            self.settings.set_string(
                "server-prefix", self.server_prefix_entry.get_text()
            )
            keyring.set_password(
                "ServerSettingsApp", "api_key", self.api_key_entry.get_text()
            )

    def run_script(self, button, filename):
        try:
            count = int(self.server_count_spinner.get_value())
            server_type = str(self.server_types_combo.get_model()[self.server_types_combo.get_active()][0])
            output = subprocess.check_output(
                ["python", filename, str(count), server_type],
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.text_buffer.set_text("")
            self.text_buffer.insert_at_cursor(f"Output from {filename}:\n{output}\n\n")
        except subprocess.CalledProcessError as e:
            self.text_buffer.insert_at_cursor(
                f"Error executing {filename}:\n{e.output}\n\n"
            )

    def on_window_destroy(self, widget):
        # Save the current value when the window is closed
        self.save_last_value()
        Gtk.main_quit()

    def load_last_value(self):
        try:
            with open("server_count.txt", "r") as file:
                last_value = int(file.read())
                self.server_count_spinner.set_value(last_value)
        except FileNotFoundError:
            pass

    def save_last_value(self):
        last_value = int(self.server_count_spinner.get_value())
        with open("server_count.txt", "w") as file:
            file.write(str(last_value))


class Application(Adw.Application):

    def __init__(self, **kwargs):
        app_id = "com.kartoza.HetznerManagement"
        super().__init__(**kwargs)
        self.connect('activate', self.do_activate)
        self.win = None
        
    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = HetznerManagement(application=self)
        win.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)


if __name__ == "__main__":

    os.environ["GSETTINGS_SCHEMA_DIR"] = (
        "/home/timlinux/dev/python/hetzner-management/schema/"
    )
    app = Application()
    sm = app.get_style_manager()
    sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
    app.run(None)
