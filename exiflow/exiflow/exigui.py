#!/usr/bin/env python2.4
# -*- coding: UTF-8 -*-

import os.path
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import exiflow.exirename

gladefile = os.path.join(sys.path[0], "exiflow", "exigui.glade")

class Filechooser1(object):
   def __init__(self, parent = None, callback=None):
      self.wTree = gtk.glade.XML(gladefile, "filechooserdialog1")
      self.window = self.wTree.get_widget("filechooserdialog1")
      dic = {}
      for key in dir(self.__class__):
         dic[key] = getattr(self, key)
      self.wTree.signal_autoconnect(dic)
      if parent:
         self.window.set_transient_for(parent)
      self.callback = callback
      self.window.show()

   def on_filechooserdialog1_response(self, widget, data = None):
      if data == gtk.RESPONSE_OK and callable(self.callback):
         self.callback(widget.get_filenames())
      self.window.destroy()


class Aboutdialog1(object):
   def __init__(self, parent = None):
      self.wTree = gtk.glade.XML(gladefile, "aboutdialog1")
      self.window = self.wTree.get_widget("aboutdialog1")
      dic = {}
      for key in dir(self.__class__):
         dic[key] = getattr(self, key)
      self.wTree.signal_autoconnect(dic)
      if parent:
         self.window.set_transient_for(parent)
      self.window.show()


class Window1(object):
   def __init__(self):
      self.wTree = gtk.glade.XML(gladefile, "mainwindow")
      self.window = self.wTree.get_widget("mainwindow")
# Initialize treeview
      treeview = self.wTree.get_widget("treeview1")
      self.liststore = gtk.ListStore(str)
      treeview.set_model(self.liststore)
      text_cell = gtk.CellRendererText()
      text_column = gtk.TreeViewColumn("Filename")
      text_column.pack_start(text_cell, True)
      text_column.add_attribute(text_cell, "text", 0)
      #text_column.set_attributes(text_cell, markup=1) #wir müssen markup anschalten um den text später formatiern zu können
      treeview.append_column(text_column)
      dic = {}
      for key in dir(self.__class__):
         dic[key] = getattr(self, key)
      self.wTree.signal_autoconnect(dic)
      self.window.show()

   def on_button_open_clicked(self, widget, data = None):
      diag = Filechooser1(self.window, self.set_filelist)

   def on_info1_activate(self, widget, data=None):
      diag = Aboutdialog1(self.window)

   def on_mainwindow_destroy(self, widget, data = None):
      gtk.main_quit()

   def set_filelist(self, files):
      self.liststore.clear()
      for file in map(os.path.abspath, files):
         if os.path.exists(file):
            self.liststore.append([file])
         else:
            print >>sys.stderr, file, "doesn't exist!"

   def on_exirename_camid_auto_activate(self, widget, data=None):
      self.wTree.get_widget("exirename_cam_id_entry").set_sensitive(False)

   def on_exirename_camid_custom_activate(self, widget, data=None):
      self.wTree.get_widget("exirename_cam_id_entry").set_sensitive(True)

   def on_exirename_artist_auto_activate(self, widget, data=None):
      self.wTree.get_widget("exirename_artist_initials_entry").set_sensitive(False)

   def on_exirename_artist_custom_activate(self, widget, data=None):
      self.wTree.get_widget("exirename_artist_initials_entry").set_sensitive(True)

   def on_exirename_activate(self, widget, data=None):
      self.wTree.get_widget("exirename_cancel_button").set_sensitive(True)
      widget.set_sensitive(False)
      args = ["-v"]
      artist_initials = self.wTree.get_widget("exirename_artist_initials_entry")
      cam_id = self.wTree.get_widget("exirename_cam_id_entry")
      if artist_initials.state != gtk.STATE_INSENSITIVE:
         args.append("--artist_initials=" + artist_initials.get_text())
      if cam_id.state != gtk.STATE_INSENSITIVE:
         args.append("--cam_id=" + cam_id.get_text())
      args += map(lambda x: x[0], self.liststore)
      print "addparms:", args
      exiflow.exirename.run(args)
      self.wTree.get_widget("exirename_cancel_button").set_sensitive(False)
      widget.set_sensitive(True)

      

def run(argv):
   win1 = Window1()
   if len(sys.argv) > 1:
      win1.set_filelist(argv)
   gtk.main()
   return 0


if __name__ == "__main__":
   run(sys.argv[1:]) 

