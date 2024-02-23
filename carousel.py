#!/usr/bin/env python
import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GObject

class ImageCarousel(Gtk.Window):
    def __init__(self):
        super().__init__(title="Image Carousel")
        self.set_default_size(800, 600)

        # Path to the "img" folder (adjust as needed)
        self.img_folder = "img"

        # Get a list of image file paths in the folder
        self.image_paths = [os.path.join(self.img_folder, filename) for filename in os.listdir(self.img_folder) if filename.lower().endswith((".jpg", ".jpeg", ".png"))]

        self.current_image_index = 0
        self.image_view = Gtk.Image()

        # Load the first image
        self.load_image()

        # Create a timer to switch images every 3 seconds
        GObject.timeout_add(3000, self.next_image)

        self.add(self.image_view)

    def load_image(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image_paths[self.current_image_index])
        self.image_view.set_from_pixbuf(pixbuf)

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.load_image()
        return True

if __name__ == "__main__":
    win = ImageCarousel()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

