##      main_button.py
#
#       Copyright 2011 Hugo Teso <hugo.teso@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from gi.repository import GLib, GObject, Gtk, Pango

import os


class MainMenuButton (Gtk.ToggleButton):
    """Launches the popup menu when clicked.

    This sits inside the main toolbar when the main menu bar is hidden. In
    addition to providing access to the app's menu associated with the main
    view, this is a little more compliant with Fitts's Law than a normal
    `Gtk.MenuBar`: our local style modifications mean that for most styles,
    when the window is fullscreened with only the "toolbar" present the
    ``(0,0)`` screen pixel hits this button.

    Support note: Compiz edge bindings sometimes get in the way of this, so
    turn those off if you want Fitts's compliance.
    """

    def __init__(self, text, menu):
        super(Gtk.ToggleButton, self).__init__()
        self.menu = menu
        hbox1 = Gtk.HBox()
        hbox2 = Gtk.HBox()
        icon = Gtk.Image()
        icon.set_from_file('logo' + os.sep + 'inguma_16.png')
        hbox1.pack_start(icon, True, True, 3)
        label = Gtk.Label(label=text)
        hbox1.pack_start(label, True, True, 3)
        arrow = Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.IN)
        hbox1.pack_start(arrow, False, False, 3)
        hbox2.pack_start(hbox1, True, True, 0)

        # Text settings
        markup = '<span font_weight="%u">%s</span>' % (
            Pango.Weight.SEMIBOLD,
            GLib.markup_escape_text(text)
        )
        label.set_markup(markup)

        self.add(hbox2)
        self.set_relief(Gtk.ReliefStyle.NORMAL)
        self.set_can_focus(True)
        self.set_can_default(False)
        self.connect("button-press-event", self.on_button_press)

        for sig in "selection-done", "deactivate", "cancel":
            menu.connect(sig, self.on_menu_dismiss)

    def on_enter(self, widget, event):
        # Not this set_state(). That one.
        #self.set_state(Gtk.StateType.PRELIGHT)
        Gtk.Widget.set_state(self, Gtk.StateType.PRELIGHT)


    def on_leave(self, widget, event):
        #self.set_state(Gtk.StateType.NORMAL)
        Gtk.Widget.set_state(self, Gtk.StateType.NORMAL)


    def on_button_press(self, widget, event):
        # Post the menu. Menu operation is much more convincing if we call
        # popup() with event details here rather than leaving it to the toggled
        # handler.
        pos_func = self._get_popup_menu_position
        self.menu.popup(None, None, pos_func, widget, event.button, event.time)
        self.set_active(True)
        self.menu.show_all()


    def on_menu_dismiss(self, *a, **kw):
        # Reset the button state when the user's finished, and
        # park focus back on the menu button.
        #self.set_state(Gtk.StateType.NORMAL)
        self.set_active(False)
        self.grab_focus()


    def _get_popup_menu_position(self, menu, *junk):
        # Underneath the button, at the same x position.
        x, y = self.get_window().get_origin()[1:]
        x += self.get_allocation().x+1
        y += self.get_allocation().y+self.get_allocation().height
        return x, y, True
