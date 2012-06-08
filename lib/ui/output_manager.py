##      output_manager.py
#
#       Copyright 2009 Hugo Teso <hugo.teso@gmail.com>
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

import os, sys
import lib.globals as glob

import gtk

# The reason for this is that PyGTK now contains an interactive event loop.
# We should switch off this event loop before starting our own event loop for
# the HTTP server to avoid the two event loops interfering with each other.
# gtk.set_interactive(True) causes gtk's event loop to run automatically
# whenever Python is waiting for the user to type in the next Python command, as in
# the main loop in raw_input. After gtk.set_interactive(False), the *automatic*
# launching of the event loop no longer happens. Otherwise, it has no effect on
# gtk's event loops.
gtk.set_interactive(False)

class OutputManager:

    def __init__(self, iface, ing=None, debug=False):

        self.ing = ing
        self.iface = iface
        self.debug = debug
        self.dot_file = ''

        if self.iface != 'gui' and self.iface != 'console':
            print "Output interface not valid, must be 'gui' or 'console'"
            sys.exit(0)

    def console(self, data=''):
        '''Helper to force output by console.'''
        print(data)

    def debug(self, data = '', window=True, newline=True):
        """ Function that will print debug messages if we enabled -d on the command line."""

        if self.debug:
            print data

    def echo(self, data = "", window=True, newline=True):
        '''Generic method for printing stuff on the UI'''

        if window == True and glob.isGui:
            window = self.SHOW_MODULE_WIN

        if self.iface == 'gui':
            if not window:
                #print "GTK UI: ", data
                enditer = self.omwidget.get_end_iter()
                if newline:
                    self.omwidget.insert(enditer, data + '\n')
                else:
                    self.omwidget.insert(enditer, data)
                #self.omwidget.set_text(data + '\n')
                self.update_helpers()
                self.alert_tab()

            else:
                if not hasattr(self, 'module_dialog'):
                    # The main window hasn't got yet proper widgets, so we fallback
                    # to console.
                    self.console(data)
                    return False

                enditer = self.module_dialog.output_buffer.get_end_iter()
                if newline:
                    self.module_dialog.output_buffer.insert(enditer, data + '\n')
                else:
                    self.module_dialog.output_buffer.insert(enditer, data)
                self.update_helpers()
                #self.omwidget.set_text(data + '\n')

        elif self.iface == 'console':
            print data

        return False

    def update_graph(self):

        f = open(self.dot_file, 'r')
        dot = f.read()
        f.close()
        self.map.set_dotcode(dot)

    def create_module_dialog(self):

        import lib.ui.ModuleDialog as ModuleDialog
        self.module_dialog = ModuleDialog.ModuleDialog()

        return False

    def set_gui(self, widget):

        self.omwidget = widget

    def set_kbwin(self, kbwin):

        self.kbwin = kbwin

    def set_map(self, map):

        self.map = map
        self.kbwin.xdot = self.map

    def set_core(self, core):

        self.uicore = core

    def set_new_nodes(self, state):

        self.newNodes = state

    def get_new_nodes(self):

        return self.newNodes

    def alert_tab(self):
        bottom_nb = self.ing.bottom_nb
        if bottom_nb.get_current_page() != 0:
            self.ing.log_icon.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)

    #
    # Listeners methods
    #

    def update_listener_status(self, host, port):
        self.echo("Updating listener %s at port %s" % (host, port), False)
        self.ing.treeview.update_listener(host, str(port))

    #
    # Statusbar output methods
    #
    def insert_sb_text(self, text):
        context = self.ing.statusbar.get_context_id(text)
        self.icon = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file('logo' + os.sep + 'inguma_16.png')
        scaled_buf = pixbuf.scale_simple(16,16,gtk.gdk.INTERP_BILINEAR)
        self.icon.set_from_pixbuf(scaled_buf)

        self.ing.statusbar.pack_start(gtk.VSeparator(), False, False, 2)
        self.ing.statusbar.pack_start(gtk.Label(text), False, False, 2)
        self.ing.statusbar.pack_start(self.icon, False, False, 2)

    def insert_bokken_text(self, data_dict, version):
        '''data_dict ontains text to be added.
           Key will be the title
           Value will be... well, the value :)'''

        context = self.ing.bokken_sb.get_context_id('sb')        
        self.text = ''
        for element in data_dict.keys():
            self.text += element.capitalize() + ': ' + str(data_dict[element]) + ' | '
        self.ing.bokken_sb.push(context, self.text)
        if version:
            self.icon = gtk.Image()
            pixbuf = gtk.gdk.pixbuf_new_from_file('lib/ui/bokken/data/icon.png')
            scaled_buf = pixbuf.scale_simple(16,16,gtk.gdk.INTERP_BILINEAR)
            self.icon.set_from_pixbuf(scaled_buf)

            self.ing.bokken_sb.pack_end(gtk.Label('Bokken ' + version), False)
            self.ing.bokken_sb.pack_end(self.icon, False, False, 2)
            self.ing.bokken_sb.pack_end(gtk.VSeparator(), False)
        #self.ing.bokken_sb.show_all()

    def clear_sb_text(self):
        context = self.ing.statusbar.get_context_id('sb')        
        self.ing.statusbar.pop(context)

    def update_helpers(self):
        core = self.ing.uicore
        targets = str(len(core.get_kbfield('targets')))
        vulns = str(core.get_vulns())
        self.ing.statusbar.update_helpers([targets, vulns, '0'])
