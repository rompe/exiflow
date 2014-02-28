#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
A nice PyGTK GUI for the exiflow tool collection.
"""
__revision__ = "$Id$"

import os
import sys
import logging
import optparse
import pygtk
import shutil
import tempfile
pygtk.require("2.0")
import gtk
import gtk.glade

from . import filelist
from . import exiassign
from . import exiconvert
from . import exigate
from . import exiimport
from . import exiperson
from . import exirename

gladefile = os.path.splitext(__file__)[0] + ".glade"


class WritableTextView(object):
    """
    Provide a file object that writes to a GTK textview.
    """
    def __init__(self, textview, color=None):
        """
        Construct the file object writing to textview, optionally using color.
        """
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
        """
        Output msg to the textview.
        """
        my_iter = self.buffer.get_end_iter()
        tag_names = self.tag_names[:]
        if msg.startswith("WARNING") or msg.startswith("ERROR"):
            tag_names.append("warning")
        self.buffer.insert_with_tags_by_name(my_iter, msg, *tag_names)
        self.textview.scroll_mark_onscreen(self.buffer.get_insert())

    def flush(self):
        """
        Imitate a buffer flush.
        Since a textview can't be flushed, do nothing.
        """
        pass


class Directorychooser1(object):
    """
    Create a window that allows the user to select a directory.
    """
    def __init__(self, parent=None, callback=None):
        """ Instantiate the chooser. """
        self.wtree = gtk.glade.XML(gladefile, "directorychooserdialog1")
        self.window = self.wtree.get_widget("directorychooserdialog1")
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.wtree.signal_autoconnect(dic)
        if parent:
            self.window.set_transient_for(parent)
        self.callback = callback
        self.window.show()

    def on_directorychooserdialog1_response(self, widget, data=None):
        """ Callback function for the chooser. """
        if data == gtk.RESPONSE_OK and callable(self.callback):
            self.callback(widget.get_filename())
        self.window.destroy()


class Filechooser1(object):
    """
    Create a window that allows the user to select files.
    """
    def __init__(self, parent=None, callback=None):
        """ Instantiate the chooser. """
        self.wtree = gtk.glade.XML(gladefile, "filechooserdialog1")
        self.window = self.wtree.get_widget("filechooserdialog1")
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.wtree.signal_autoconnect(dic)
        if parent:
            self.window.set_transient_for(parent)
        self.callback = callback
        self.window.show()

    def on_filechooserdialog1_response(self, widget, data=None):
        """ Callback function for the chooser. """
        if data == gtk.RESPONSE_OK and callable(self.callback):
            self.callback(widget.get_filenames())
        self.window.destroy()


class Window1(object):
    """
    The program's main window.
    """
    def __init__(self):
        """ Instantiate the main window. """
        self._cancelled = False
        self.wtree = gtk.glade.XML(gladefile, "mainwindow")
        self.window = self.wtree.get_widget("mainwindow")
        # Initialize treeview
        treeview = self.wtree.get_widget("treeview1")
        self.liststore = gtk.ListStore(str)
        treeview.set_model(self.liststore)
        text_cell = gtk.CellRendererText()
        text_column = gtk.TreeViewColumn("Filename")
        text_column.pack_start(text_cell, True)
        text_column.add_attribute(text_cell, "text", 0)
        #text_column.set_attributes(text_cell, markup=1)
        #wir müssen markup anschalten um den text später formatieren zu können
        treeview.append_column(text_column)
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.wtree.signal_autoconnect(dic)
        self.window.show()
        # Create TextView and use it
        sys.stdout = WritableTextView(self.wtree.get_widget("textview1"))
        sys.stderr = WritableTextView(self.wtree.get_widget("textview1"),
                                      "blue")
        stdlog = WritableTextView(self.wtree.get_widget("textview1"), "red")
        logging.basicConfig(format="%(module)s: %(message)s", stream=stdlog,
                            level=logging.INFO)
        self.batch_scripts = []
        self.batch_tmpdir = ""
        self.batch_target = ""
        self.window.connect("map_event", self.batch_run)

    def _make_sensitive(self, name):
        """ Set widget called name sensitive. """
        self.wtree.get_widget(name).set_sensitive(True)

    def _make_insensitive(self, name):
        """ Set widget called name insensitive. """
        self.wtree.get_widget(name).set_sensitive(False)

    def _is_active(self, name):
        """ Return True if widget "name" is activated, False otherwise. """
        return self.wtree.get_widget(name).get_active()

    def set_active(self, name):
        """ Activate button of widget "name". """
        self.wtree.get_widget(name).set_active(1)

    def set_text(self, name, text):
        """ Set text of widget "name" to text. """
        self.wtree.get_widget(name).set_text(text)

    def on_button_open_clicked(self, *dummy):
        """ Callback for the "open" button. """
        dummy = Filechooser1(self.window, self.set_filelist)

    def on_button_exiimport_browse_importdir_clicked(self, *dummy):
        """ Callback for the exiimport's "browse importdir" button. """
        dummy = Directorychooser1(self.window,
                                  self.wtree.get_widget(
                                      "exiimport_importdir_entry").set_text)

    def on_button_exiimport_browse_targetdir_clicked(self, *dummy):
        """ Callback for the exiimport's "browse targetdir" button. """
        dummy = Directorychooser1(self.window,
                                  self.wtree.get_widget(
                                      "exiimport_targetdir_entry").set_text)

    @staticmethod
    def on_info1_activate(*dummy):
        """ Callback for the "about" menu entry. """
        wtree = gtk.glade.XML(gladefile, "aboutdialog1")
        window = wtree.get_widget("aboutdialog1")
        window.show_all()
        window.run()
        window.hide()

    @staticmethod
    def on_mainwindow_destroy(*dummy):
        """ Callback for the window's close button. """
        gtk.main_quit()

    def set_filelist(self, files):
        """
        Put files into the filelist.
        Directories are extrapolated via the Filelist class.
        """
        logger = logging.getLogger("exigui.set_filelist")
        self.liststore.clear()
        for filename in filelist.Filelist(files).get_files():
            filename = os.path.abspath(filename)
            if os.path.exists(filename):
                self.liststore.append([filename])
            else:
                logger.warning("%s doesn't exist!", filename)

    def on_exirename_camid_auto_activate(self, *dummy):
        """ Callback for exirename's "auto cam_id" selection. """
        self._make_insensitive("exirename_cam_id_entry")

    def on_exirename_camid_custom_activate(self, *dummy):
        """ Callback for exirename's "custom cam_id" selection. """
        self._make_sensitive("exirename_cam_id_entry")

    def on_exirename_artist_auto_activate(self, *dummy):
        """ Callback for exirename's "auto artist" selection. """
        self._make_insensitive("exirename_artist_initials_entry")

    def on_exirename_artist_custom_activate(self, *dummy):
        """ Callback for exirename's "custom artist" selection. """
        self._make_sensitive("exirename_artist_initials_entry")

    def on_exiperson_section_auto_activate(self, *dummy):
        """ Callback for exirename's "auto section" selection. """
        self._make_insensitive("exiperson_section_entry")

    def on_exiperson_section_custom_activate(self, *dummy):
        """ Callback for exirename's "custom section" selection. """
        self._make_sensitive("exiperson_section_entry")

    def _progress_callback(self, filename, newname, percentage,
                           keep_original=False):
        """
        This callback is given as a callable to the main programs and is
        called after each processed file. filename and newname may of course
        be the same. If keep_original is True, add newname instead of replacing
        filename with it.
        Return self._cancelled which is True after Cancel has been pressed.
        """
        if filename != newname:
            if keep_original:
                self.liststore.append([newname])
            else:
                for rownum in range(0, len(self.liststore)):
                    if self.liststore[rownum][0] == filename:
                        self.liststore[rownum][0] = newname
        nbook = self.wtree.get_widget("notebook1")
        tab = nbook.get_tab_label(nbook.get_nth_page(nbook.get_current_page()))
        label = tab.get_text()
        progressbar = self.wtree.get_widget("progressbar1")
        progressbar.set_fraction(float(percentage) / 100)
        progressbar.set_text(u"%s:   %s %%" % (label, percentage))
        while gtk.events_pending():
            gtk.main_iteration(False)
        return self._cancelled

    def on_cancel_activate(self, widget, *dummy):
        """
        Called from the cancel button.
        """
        logger = logging.getLogger("exigui.on_cancel_activate")
        self._cancelled = True
        widget.set_sensitive(False)
        logger.warning("CANCELLED!")

    def on_run_activate(self, widget, *dummy):
        """
        Called from the run button.
        """
        logger = logging.getLogger("exigui.on_run_activate")
        cancel_button = self.wtree.get_widget("cancel_button")
        cancel_button.set_sensitive(True)
        nbook = self.wtree.get_widget("notebook1")
        nbook.set_sensitive(False)
        widget.set_sensitive(False)
        self._cancelled = False

        tab = nbook.get_tab_label(nbook.get_nth_page(nbook.get_current_page()))
        label = tab.get_text()
        logger.warning("Running %s", label)
        method = getattr(self, "_run_" + label.replace(" ", "_"))
        method()

        progressbar = self.wtree.get_widget("progressbar1")
        progressbar.set_fraction(0 / 100)
        progressbar.set_text(u"")
        nbook.set_sensitive(True)
        cancel_button.set_sensitive(False)
        widget.set_sensitive(True)

    def _run_exiimport(self):
        """ Run exiimport. """
        logger = logging.getLogger("exigui.run_exiimport")
        args = ["-v"]
        import_dir = self.wtree.get_widget("exiimport_importdir_entry")
        target_dir = self.wtree.get_widget("exiimport_targetdir_entry")
        if import_dir.get_text():
            args.append("--mount=" + import_dir.get_text())
        if target_dir.get_text():
            args.append("--target=" + target_dir.get_text())
        try:
            exiimport.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def _run_exirename(self):
        """ Run exirename. """
        logger = logging.getLogger("exigui.run_exirename")
        args = ["-v"]
        initials = self.wtree.get_widget("exirename_artist_initials_entry")
        cam_id = self.wtree.get_widget("exirename_cam_id_entry")
        if self._is_active("exirename_artist_initials_entry_button_custom"):
            args.append("--artist_initials=" + initials.get_text())
        if self._is_active("exirename_cam_id_entry_button_custom"):
            args.append("--cam_id=" + cam_id.get_text())
        if self._is_active("exirename_include_timestamp_checkbutton"):
            args.append("--with_time")
        args += [entry[0] for entry in self.liststore]
        try:
            exirename.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def _run_exiperson(self):
        """ Run exiperson. """
        logger = logging.getLogger("exigui.run_exiperson")
        args = ["-v"]
        exif_section = self.wtree.get_widget("exiperson_section_entry")
        if self._is_active("exiperson_section_entry_button_custom"):
            args.append("--section=" + exif_section.get_text())
        args += [entry[0] for entry in self.liststore]
        try:
            exiperson.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def _run_exiconvert(self):
        """ Run exiconvert. """
        logger = logging.getLogger("exigui.run_exiconvert")
        args = ["-v"]
        if self._is_active("exiconvert_remove_lqjpeg_checkbutton"):
            args.append("--remove-lqjpeg")
        args += [entry[0] for entry in self.liststore]
        try:
            exiconvert.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def _run_exiassign(self):
        """ Run exiassign. """
        logger = logging.getLogger("exigui.run_exiassign")
        args = ["-v"]
        if self._is_active("exiassign_force_checkbutton"):
            args.append("--force")
        args += [entry[0] for entry in self.liststore]
        try:
            exiassign.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def _run_exigate(self):
        """ Run exigate. """
        logger = logging.getLogger("exigui.run_exigate")
        if self._is_active("exigate_nooptions"):
            args = ["-v"]
        if self._is_active("exigate_addfields"):
            args = ["--additional-fields"]
        if self._is_active("exigate_template"):
            args = ["--template"]
        if self._is_active("exigate_cleanup"):
            args = ["--cleanup"]
        args.append("-v")
        args += [entry[0] for entry in self.liststore]
        try:
            exigate.run(args, self._progress_callback)
        except IOError, msg:
            logger.error("ERROR: %s", msg)

    def batch_run(self, *dummy):
        """ Run "scripts" in a batch without user interaction. """
        if len(self.batch_scripts) > 0:
            logger = logging.getLogger("exigui.batch_run")
            nbook = self.wtree.get_widget("notebook1")
            tabs = []
            for tabnum in range(0, nbook.get_n_pages()):
                tab_label = nbook.get_tab_label(nbook.get_nth_page(tabnum))
                tabs.append(tab_label.get_text())
            for script in self.batch_scripts:
                if script not in tabs:
                    logger.error("There is no %s tab available!", script)
                    return 1
            run_button = self.wtree.get_widget("activate_button")
            for script in self.batch_scripts:
                nbook.set_current_page(tabs.index(script))
                self.on_run_activate(run_button)
            self.batch_scripts = []
            if self.batch_tmpdir:
                self.set_text("exiimport_targetdir_entry", self.batch_target)
                for subdir in os.listdir(self.batch_tmpdir):
                    target_subdir = subdir
                    while os.path.exists(os.path.join(self.batch_target,
                                                      target_subdir)):
                        logger.warning("%s already exists!",
                                       os.path.join(self.batch_target,
                                                    target_subdir))
                        target_subdir += "+"
                    logger.info("Moving %s into target directory %s", subdir,
                                os.path.join(self.batch_target, target_subdir))
                    try:
                        shutil.move(os.path.join(self.batch_tmpdir, subdir),
                                    os.path.join(self.batch_target,
                                                 target_subdir))
                    except shutil.Error, msg:
                        logger.error("ERROR: %s", msg)
                    for rownum in range(0, len(self.liststore)):
                        self.liststore[rownum][0] = \
                            self.liststore[rownum][0].replace(
                                os.path.join(self.batch_tmpdir, subdir),
                                os.path.join(self.batch_target, target_subdir))

        return 0


def run(argv):
    """
    Take an equivalent of sys.argv[1:] and run the GUI.
    """
    parser = optparse.OptionParser()
    parser.set_defaults(batch_order="exiimport,exirename,exiperson,"
                                    "exiconvert,exiassign,exigate")
    parser.add_option("-m", "--mount", dest="mount",
                      help="Mountpoint of directory to import.")
    parser.add_option("-t", "--target", dest="target",
                      help="Target directory. A subdirectory will be created"
                      " in this directory.")
    parser.add_option("-d", "--device", dest="device",
                      help="(Ignored for backwards compatibility. Don't use.)")
    parser.add_option("--cam_id", "-c", dest="cam_id",
                      help="ID string for the camera model. Should normally be"
                      " three characters long.")
    parser.add_option("--artist_initials", "-a", dest="artist_initials",
                      help="Initials of the artist. Should be two characters"
                      " long.")
    parser.add_option("-T", "--with_time", action="store_true",
                      dest="with_time",
                      help="Create filenames containing the image time, for"
                      " example 20071231-235959-n001234-xy000.jpg instead"
                      " of 20071231-n001234-xy000.jpg .")
    parser.add_option("-b", "--batch", action="store_true", dest="batch",
                      help="Autorun from exiimport over exirename, exiperson "
                      "and exiconvert to exiassign.")
    parser.add_option("--batch_order",
                      help="Comma separated processing order for --batch. "
                      "Default: %default")
    parser.add_option("--batch_tmpdir",
                      help="If the processing order starts with 'exiimport', "
                      "this temporary directory is used for batch processing. "
                      "After batch processing, the created subdirectory will "
                      "be moved into the target directory.")
    parser.add_option("--nofork", action="store_true",
                      help="Do not fork, stay in foreground instead.")
    options, args = parser.parse_args(argv)

    if options.nofork or os.fork() == 0:
        win1 = Window1()
        if options.mount:
            win1.set_text("exiimport_importdir_entry", options.mount)
        if options.target:
            win1.set_text("exiimport_targetdir_entry", options.target)
        if options.cam_id:
            win1.set_active("exirename_cam_id_entry_button_custom")
            win1.set_text("exirename_cam_id_entry", options.cam_id)
        if options.artist_initials:
            win1.set_active("exirename_artist_initials_entry_button_custom")
            win1.set_text("exirename_artist_initials_entry",
                          options.artist_initials)
        if options.with_time:
            win1.set_active("exirename_include_timestamp_checkbutton")
        if len(args) > 0:
            win1.set_filelist(args)
        if options.batch:
            win1.batch_scripts = options.batch_order.split(',')
            if options.batch_tmpdir and "exiimport" in win1.batch_scripts:
                if not options.mount or not options.target:
                    print("Wrong syntax. Missing --mount or --target\n"
                          + parser.format_help())
                    win1.batch_scripts = []
                win1.batch_tmpdir = tempfile.mkdtemp(dir=options.batch_tmpdir)
                win1.batch_target = options.target
                win1.set_text("exiimport_targetdir_entry", win1.batch_tmpdir)

        gtk.main()

    return 0


if __name__ == "__main__":
    run(sys.argv[1:])
