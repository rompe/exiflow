#!/usr/bin/env python2.4
# -*- coding: UTF-8 -*-

import os.path
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import exiflow.exiassign
import exiflow.exigate
import exiflow.exiperson
import exiflow.exirename

gladefile = os.path.join(sys.path[0], "exiflow", "exigui.glade")


class WritableTextView:
   def __init__(self, textview, color=None):
      self.textview = textview
      self.buffer = self.textview.get_buffer()
      self.tag_names = []
      tag_table = self.buffer.get_tag_table()
      if not tag_table.lookup("warning"):
         tag = gtk.TextTag("warning")
         tag.set_property("foreground", "red")
         tag.set_property("background", "yellow")
         tag_table.add(tag)
      if color:
         if not tag_table.lookup(color):
            tag = gtk.TextTag(color)
            tag.set_property("foreground", color)
            tag_table.add(tag)
         self.tag_names.append(color)

   def write(self, msg):		
      iter = self.buffer.get_end_iter()
      tag_names = self.tag_names[:]
      if msg.startswith("WARNING") or msg.startswith("ERROR"):
         tag_names.append("warning")
      self.buffer.insert_with_tags_by_name(iter, msg, *tag_names)
      self.textview.scroll_mark_onscreen(self.buffer.get_insert())


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
# Create TextView and use it
      sys.stdout = WritableTextView(self.wTree.get_widget("textview1"))
      sys.stderr = WritableTextView(self.wTree.get_widget("textview1"), "blue")

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

   def on_exiperson_section_auto_activate(self, widget, data=None):
      self.wTree.get_widget("exiperson_section_entry").set_sensitive(False)

   def on_exiperson_section_custom_activate(self, widget, data=None):
      self.wTree.get_widget("exiperson_section_entry").set_sensitive(True)

   def _progress_callback(self, filename, newname, percentage):
      """
      This callback is given as a callable to the main programs and is
      called after each processed file. filename and newname may of course
      be the same. Return self._cancelled which is True when Cancel is pressed.
      """
      if filename != newname:
         for rownum in range(0, len(self.liststore)):
            if self.liststore[rownum][0] == filename:
               self.liststore[rownum][0] = newname
      progressbar = self.wTree.get_widget("progressbar1")
      progressbar.set_fraction(float(percentage) / 100)
      progressbar.set_text(u"%s %%" % percentage)
      while gtk.events_pending():
         gtk.main_iteration(False)
      return self._cancelled
      
   def on_cancel_activate(self, widget, data=None):
      """
      Called from the cancel button.
      """
      self._cancelled = True
      widget.set_sensitive(False)
      sys.stderr.write("CANCELLED!\n")

   def on_run_activate(self, widget, data=None):
      """
      Called from the run button.
      """
      cancel_button = self.wTree.get_widget("cancel_button")
      cancel_button.set_sensitive(True)
      nbook = self.wTree.get_widget("notebook1")
      nbook.set_sensitive(False)
      widget.set_sensitive(False)
      self._cancelled = False
      
      label = nbook.get_tab_label(nbook.get_nth_page(nbook.get_current_page())).get_text()
      sys.stderr.write("Running %s\n" % label)
      method = getattr(self, "run_" + label.replace(" ", "_"))
      method()
      
      nbook.set_sensitive(True)
      cancel_button.set_sensitive(False)
      widget.set_sensitive(True)

   def run_exirename(self):
      args = ["-v"]
      artist_initials = self.wTree.get_widget("exirename_artist_initials_entry")
      cam_id = self.wTree.get_widget("exirename_cam_id_entry")
      if artist_initials.state != gtk.STATE_INSENSITIVE:
         args.append("--artist_initials=" + artist_initials.get_text())
      if cam_id.state != gtk.STATE_INSENSITIVE:
         args.append("--cam_id=" + cam_id.get_text())
      args += map(lambda x: x[0], self.liststore)
      try:
         exiflow.exirename.run(args, self._progress_callback)
      except IOError, msg:
         sys.stdout.write("\nERROR: %s\n" % str(msg))

   def run_exiassign(self):
      args = ["-v"]
      forcebutton = self.wTree.get_widget("exiassign_force_checkbutton")
      if forcebutton.get_active() == True:
         args.append("--force")
      args += map(lambda x: x[0], self.liststore)
      try:
         exiflow.exiassign.run(args, self._progress_callback)
      except IOError, msg:
         sys.stdout.write("\nERROR: %s\n" % str(msg))

   def run_exiperson(self):
      args = ["-v"]
      exif_section = self.wTree.get_widget("exiperson_section_entry")
      if exif_section.state != gtk.STATE_INSENSITIVE:
         args.append("--section=" + exif_section.get_text())
      args += map(lambda x: x[0], self.liststore)
      try:
         exiflow.exiperson.run(args, self._progress_callback)
      except IOError, msg:
         sys.stdout.write("\nERROR: %s\n" % str(msg))
      
   def run_exigate_gthumb(self):
      if self.wTree.get_widget("exigate_gthumb_nooptions").get_active() == True:
         args = ["-v"]
      if self.wTree.get_widget("exigate_gthumb_addfields").get_active() == True:
         args = ["--additional-fields"]
      if self.wTree.get_widget("exigate_gthumb_template").get_active() == True:
         args = ["--template"]
      if self.wTree.get_widget("exigate_gthumb_cleanup").get_active() == True:
         args = ["--cleanup"]
      args.append("-v")
      args += map(lambda x: x[0], self.liststore)
      try:
         exiflow.exigate.run(args, self._progress_callback)
      except IOError, msg:
         sys.stdout.write("\nERROR: %s\n" % str(msg))

def run(argv):
   win1 = Window1()
   if len(sys.argv) > 1:
      win1.set_filelist(argv)
   gtk.main()
   return 0


if __name__ == "__main__":
   run(sys.argv[1:]) 

