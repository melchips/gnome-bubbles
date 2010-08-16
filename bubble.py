#!/usr/bin/env python

#    This file is part of gnome-bubbles.
#
#    gnome-bubbles is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    gnome-bubbles is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with gnome-bubbles.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import gtk
import subprocess
import webkit
from inspector import Inspector
import bblbox

""" A bubble is a window with an embedded browser that can be minimised in the task bar """
class Bubble:
    def __init__(self, bblbox_to_load):
        self.bblbox_loaded = bblbox.Bblbox(bblbox_to_load)
        self.bblbox_loaded.parse()
        self.webpage_to_load = self.bblbox_loaded.get_url()
        print self.webpage_to_load
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file("gnome-bubbles.svg")
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.status_icon.set_tooltip("gnome-bubbles")
        self.window = gtk.Window()
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.connect("delete-event", self.delete_event)
        self.window.connect("key-press-event", self.keypress_event)
        self.status_icon.connect('activate', self.status_clicked )
        self.is_visible = True
        self.browser = webkit.WebView()
        settings = self.browser.get_settings()
        settings.set_property("enable-developer-extras", True)
        self.browser.connect('title-changed', self.title_changed)
#        self.browser.connect('url-changed',self.url_changed)

        box = gtk.VBox(homogeneous=False, spacing=0)
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)

        self.window.set_default_size(200, 300)
        self.window.set_resizable(True)
        self.window.set_icon_from_file("gnome-bubbles.svg")

        box.pack_start(self.browser, expand=True, fill=True, padding=0)
        scrolled_window.add(box)
        self.window.add(scrolled_window)
        self.browser.open(self.webpage_to_load)
        self.browser.connect('load-finished', self.finished_loading)
        inspector = Inspector(self.browser.get_web_inspector())
        scrolled_window.show_all()
        self.window.show_all()

    def right_click_event(self, icon, button, time):
        menu = gtk.Menu()

        about = gtk.MenuItem("About")
        quit = gtk.MenuItem("Quit")

        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", gtk.main_quit)

        menu.append(about)
        menu.append(quit)
        menu.show_all()

        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.status_icon)

    def show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()

		about_dialog.set_destroy_with_parent(True)
		about_dialog.set_name("gnome-bubbles")
		about_dialog.set_version("1.0")
		about_dialog.set_authors(["melchips"])
		about_dialog.set_logo(gtk.gdk.pixbuf_new_from_file("gnome-bubbles.svg"))
		about_dialog.set_icon_from_file("gnome-bubbles.svg")

		about_dialog.run()
		about_dialog.destroy()

    def delete_event(self,window,event):
        #don't delete; hide instead
        self.window.hide_on_delete()
        self.is_visible = False
        return True

    def status_clicked(self,status):
        #unhide the window
        if (self.is_visible):
            self.window.hide_on_delete()
            self.is_visible=False
        else:
            self.window.show_all()
            self.is_visible=True

    def keypress_event(self, widget, event):
        if event.keyval == gtk.keysyms.Escape:
            self.window.hide_on_delete()
            self.is_visible = False

    def title_changed(self, widget, frame, title):
        if title != 'null':
            if len(title)>14 and title[0:14]=="GNOME-BUBBLES:":
                print "TO IMPLEMENT : action" + title[14:len(title)]
            else:
                self.status_icon.set_tooltip(title)
                print "title="+title

    def read_javascript(self, filename):
        with open(filename, 'r') as f:
            read_data = f.read()
        f.closed
        return read_data

#    def url_changed(self, url):
#        self.browser.execute_script(self.read_javascript("gnome-bubbles-framework.js"))

    def finished_loading(self, view, frame):
        self.browser.execute_script(self.read_javascript("gnome-bubbles-framework.js"))
        self.browser.execute_script(self.bblbox_loaded.get_data())

    def notify(self, head, msg):
        subprocess.call(['notify-send', head, msg])

    def contextMenu_click(self, widget):
        print "click"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch a bubble')
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('bblbox_to_load', help='.bblbox file to load')
    args = parser.parse_args()
    if (args.bblbox_to_load):
        Bubble(args.bblbox_to_load)
        gtk.main()
    else:
        parser.print_help()

