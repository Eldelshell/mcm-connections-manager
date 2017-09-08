# - coding: utf-8 -
#
# Copyright (C) 2010 Alejandro Ayuso
#
# This file is part of the MCM Connection Manager
#
# MCM Connection Manager is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MCM Connection Manager is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with the MCM Connection Manager. If not, see
# <http://www.gnu.org/licenses/>.
#

import gtk
import gtkvnc
import mcm.gui.widgets
from time import strftime
import mcm.common.constants as constants

full_depth = "Full (All Colors)"
medium_depth = "Medium (256)"
low_depth = "Low (64)"
ultra_low_depth = "Ultra Low (8)"

class MCMVncClient(object):
    def __init__(self, host, port, raw_depth, view_only):
        self.host = host
        self.port = port
        self.depth = self.parse_depth(raw_depth)
        self.view_only = view_only
        self.vnc = self.new_vnc_client()
        #self.menu = self.new_vnc_menu()
        self.layout = gtk.VBox()
        self.scroll = gtk.ScrolledWindow()
        self.scroll.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        self.scroll.add_with_viewport(self.vnc)
        self.scroll.show_all()
        #self.layout.pack_start(self.menu, False, True, 0)
        self.layout.pack_start(self.scroll, True, True, 0)

    def new_vnc_client(self):
        # We add any configuration here
        v = gtkvnc.Display()
        v.set_pointer_grab(True)
        v.set_keyboard_grab(True)
        v.set_read_only(self.view_only)
        v.set_depth(self.depth)
        v.connect("vnc-connected", self.vnc_connected)
        v.connect("vnc-disconnected", self.vnc_connected)
        v.connect("vnc-auth-credential", self.vnc_auth_cred)
        v.connect("vnc-auth-failure", self.vnc_auth_fail)
        return v

    def get_vnc_menu(self):
        menubar = gtk.MenuBar()

        sendkeys = gtk.MenuItem(constants.tools)
        menubar.append(sendkeys)

        scrs = gtk.MenuItem(constants.screenshot)
        caf1 = gtk.MenuItem("Ctrl+Alt+F_1")
        caf7 = gtk.MenuItem("Ctrl+Alt+F_7")
        cad = gtk.MenuItem("Ctrl+Alt+_Del")
        cab = gtk.MenuItem("Ctrl+Alt+_Backspace")
        disc = gtk.MenuItem(constants.disconnect)
        sep = gtk.SeparatorMenuItem()

        submenu = gtk.Menu()
        submenu.append(caf1)
        submenu.append(caf7)
        submenu.append(cad)
        submenu.append(cab)
        submenu.append(sep)
        submenu.append(scrs)
        submenu.append(disc)
        #sendkeys.set_submenu(submenu)

        caf1.connect("activate", self.send_caf1)
        caf7.connect("activate", self.send_caf7)
        cad.connect("activate", self.send_cad)
        cab.connect("activate", self.send_cab)
        scrs.connect("activate", self.screenshot_event)
        disc.connect("activate", self.disconnect_event)
        return submenu

    def get_instance(self):
        self.vnc.open_host(self.host, self.port)
        return self.layout

    def vnc_connected(self, widget):
        pass

    def send_caf1(self, menuitem):
        self.vnc.send_keys(["Control_L", "Alt_L", "F1"])

    def send_caf7(self, menuitem):
        self.vnc.send_keys(["Control_L", "Alt_L", "F7"])

    def send_cad(self, menuitem):
        self.vnc.send_keys(["Control_L", "Alt_L", "Del"])

    def send_cab(self, menuitem):
        self.vnc.send_keys(["Control_L", "Alt_L", "BackSpace"])

    def screenshot_event(self, menuitem):
        filename = "/tmp/mcm_vnc_screenshot_%s.png" % strftime("%Y%m%d.%H%M%S")
        mcm.gui.widgets.show_info_dialog(constants.screenshot_info, filename)
        pix = self.vnc.get_pixbuf()
        pix.save(filename, "png", { "tEXt::Generator App": "MCM Connections Manager" })

    def disconnect_event(self, menuitem):
        self.vnc.close()
    
    def vnc_auth_fail(self, widget, msg):
        mcm.gui.widgets.show_error_dialog("Authentication Failed", msg)
        
    def parse_depth(self, raw):
        if full_depth == raw:
            return gtkvnc.DEPTH_COLOR_FULL
        elif medium_depth == raw:
            return gtkvnc.DEPTH_COLOR_MEDIUM
        elif low_depth == raw:
            return gtkvnc.DEPTH_COLOR_LOW
        elif ultra_low_depth == raw:
            return gtkvnc.DEPTH_COLOR_ULTRA_LOW
        else:
            return gtkvnc.DEPTH_COLOR_DEFAULT
        
    def vnc_auth_cred(self, src, credList):
        prompt = 0
        data = []
    
        for i in range(len(credList)):
            data.append(None)
            if credList[i] in (gtkvnc.CREDENTIAL_USERNAME, gtkvnc.CREDENTIAL_PASSWORD):
                prompt = prompt + 1
            elif credList[i] == gtkvnc.CREDENTIAL_CLIENTNAME:
                data[i] = "mcm"
    
        if prompt:
            dialog = gtk.Dialog(constants.auth_required, None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            label = []
            entry = []
    
            box = gtk.Table(2, prompt)
    
            row = 0
            for i in range(len(credList)):
                entry.append(gtk.Entry())
                if credList[i] == gtkvnc.CREDENTIAL_USERNAME:
                    label.append(gtk.Label("Username:"))
                elif credList[i] == gtkvnc.CREDENTIAL_PASSWORD:
                    label.append(gtk.Label("Password:"))
                    entry[-1].set_visibility(False)
                    entry[-1].set_activates_default(True)
                else:
                    entry[-1].destroy()
                    continue
    
                box.attach(label[row], 0, 1, row, row+1, 0, 0, 3, 3)
                box.attach(entry[row], 1, 2, row, row+1, 0, 0, 3, 3)
                row = row + 1
    
            vbox = dialog.get_child()
            vbox.add(box)
    
            dialog.show_all()
            res = dialog.run()
            dialog.hide()
    
            if res == gtk.RESPONSE_OK:
                row = 0
                for i in range(len(credList)):
                    if credList[i] in (gtkvnc.CREDENTIAL_USERNAME, gtkvnc.CREDENTIAL_PASSWORD):
                        data[i] = entry[row].get_text()
                        row = row + 1
    
            dialog.destroy()
    
        for i in range(len(credList)):
            if i < len(data) and data[i] != None:
                if src.set_credential(credList[i], data[i]):
                    print "Cannot set credential type %d" % (credList[i])
                    src.close()
            else:
                print "Unsupported credential type %d" % (credList[i])
                src.close()


class MCMVncOptionsDialog(object):
    
    def __init__(self):
        self.response = gtk.RESPONSE_CANCEL
        self.depth = None
        self.is_view_only = False
    
    def run(self):
        dlg = gtk.Dialog(constants.vnc_options,
             None, gtk.DIALOG_MODAL,
             ( gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
               gtk.STOCK_OK, gtk.RESPONSE_OK ))
        dlg.set_default_response(gtk.RESPONSE_CANCEL)
        dlg.connect('response', self.vnc_options_dialog_response)
        
        store = gtk.ListStore(str)
        store.append([full_depth])
        store.append([medium_depth])
        store.append([low_depth])
        store.append([ultra_low_depth])
        
        combo = gtk.ComboBox()
        combo.set_model(store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        combo.set_active(0)
        
        read_only = gtk.CheckButton(constants.view_only)
        read_only.set_active(False)
        dlg.get_content_area().pack_start(combo, False, True, 0)
        dlg.get_content_area().pack_start(read_only, False, True, 1)
        dlg.show_all()
        dlg.run()
        return (combo.get_active_text(), read_only.get_active())
        
    def vnc_options_dialog_response(self, dlg, response_id):
        if response_id == gtk.RESPONSE_OK:
            self.response = gtk.RESPONSE_OK
        dlg.destroy()