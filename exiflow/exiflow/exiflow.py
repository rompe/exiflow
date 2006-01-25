#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade


class Filechooser1(object):
   def __init__(self, parent = None, callback=None):
      self.wTree = gtk.glade.XML("exiflow.glade", "filechooserdialog1")
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
      self.wTree = gtk.glade.XML("exiflow.glade", "aboutdialog1")
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
      self.wTree = gtk.glade.XML("exiflow.glade", "window1")
      self.window = self.wTree.get_widget("window1")
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

   def on_window1_destroy(self, widget, data = None):
      gtk.main_quit()

   def set_filelist(self, files):
      print "FILES:", files
      self.liststore.clear()
      for file in files:
         self.liststore.append([file])


def main():
   win1 = Window1()
   gtk.main()
   return 0


if __name__ == "__main__":
   main() 

