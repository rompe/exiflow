#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""A nice PyGTK GUI for the exiflow tool collection."""
__revision__ = "$Id$"

import os
import sys
import logging
import argparse
import shutil
import tempfile
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

# import pygtk
# pygtk.require("2.0")
# import gtk
# import gtk.glade

# PyGObject
import gi
from gi.repository import Gtk

from . import filelist
from . import exiassign
from . import exiconvert
from . import exigate
from . import exiimport
from . import exiperson
from . import exirename

gi.require_version("Gtk", "3.0")
gladefile = os.path.splitext(__file__)[0] + ".builder"


class WritableTextView():
    """Provide a file object that writes to a GTK textview."""

    def __init__(self, textview: Gtk.TextView, color: Optional[str] = None):
        """Construct file object, write to textview, optionally use color."""
        self.textview = textview
        self.buffer = self.textview.get_buffer()
        self.tag_names: List[str] = []
        tag_table = self.buffer.get_tag_table()
        if not tag_table.lookup("warning"):
            tag = Gtk.TextTag()
            tag.set_property("foreground", "red")
            tag.set_property("background", "yellow")
            tag_table.add(tag)  # type: ignore
        if color:
            if not tag_table.lookup(color):
                tag = Gtk.TextTag()
                tag.set_property("foreground", color)
                tag_table.add(tag)  # type: ignore
#             self.tag_names.append(color)

    def write(self, msg: str):
        """Output msg to the textview."""
        my_iter = self.buffer.get_end_iter()
        tag_names = self.tag_names[:]
        if msg.startswith("WARNING") or msg.startswith("ERROR"):
            tag_names.append("warning")
        self.buffer.insert_with_tags_by_name(my_iter, msg, *tag_names)
        self.textview.scroll_mark_onscreen(  # type: ignore
            self.buffer.get_insert())  # type: ignore

    def flush(self):
        """
        Imitate a buffer flush.

        Since a textview can't be flushed, do nothing.
        """
        pass


class Directorychooser1():
    """Create a window that allows the user to select a directory."""

    def __init__(self, parent: Optional[Gtk.Window] = None,
                 callback: Optional[Callable[[str], None]] = None):
        """Instantiate the chooser."""
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file(  # type: ignore
            gladefile, ("directorychooserdialog1",))  # type: ignore
        self.window = self.builder.get_object("directorychooserdialog1")
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.builder.connect_signals(dic)
        if parent:
            self.window.set_transient_for(parent)  # type: ignore
        self.callback = callback
        self.window.show()  # type: ignore

    def on_directorychooserdialog1_response(self, widget: Gtk.Widget,
                                            data: Optional[int] = None):
        """Act as callback function for the chooser."""
        if data == Gtk.RESPONSE_OK and callable(self.callback):  # type: ignore
            self.callback(widget.get_filename())  # type: ignore
        self.window.destroy()  # type: ignore


class Filechooser1():
    """Create a window that allows the user to select files."""

    def __init__(self, parent: Optional[Gtk.Window] = None,
                 callback: Optional[Callable[[Sequence[str]], None]] = None):
        """Instantiate the chooser."""
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file(  # type: ignore
            gladefile, ("filechooserdialog1",))  # type: ignore
        self.window = self.builder.get_object("filechooserdialog1")
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.builder.connect_signals(dic)
        if parent:
            self.window.set_transient_for(parent)  # type: ignore
        self.callback = callback
        self.window.show()  # type: ignore

    def on_filechooserdialog1_response(self, widget: Gtk.Widget,
                                       data: Optional[int] = None):
        """Act as callback function for the chooser."""
        if data == Gtk.RESPONSE_OK and callable(self.callback):  # type: ignore
            self.callback(widget.get_filenames())  # type: ignore
        self.window.destroy()  # type: ignore


class Window1():
    """The program's main window."""

    def __init__(self):
        """Instantiate the main window."""
        self._cancelled = False
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file(  # type: ignore
            gladefile, ("mainwindow",))  # type: ignore
        self.window = self.builder.get_object("mainwindow")
        # builder.add_from_file(gladefile)
        # self.wtree = gtk.glade.XML(gladefile, "mainwindow")
        # Initialize treeview
        treeview = self.builder.get_object("treeview1")
        self.liststore = Gtk.ListStore(str)
        treeview.set_model(self.liststore)  # type: ignore
        text_cell = Gtk.CellRendererText()
        text_column = Gtk.TreeViewColumn("Filename")
        text_column.pack_start(text_cell, True)
        text_column.add_attribute(text_cell, "text", 0)
        # text_column.set_attributes(text_cell, markup=1)
        # wir müssen markup anschalten um den text später formatieren zu können
        treeview.append_column(text_column)  # type: ignore
        dic = {}
        for key in dir(self.__class__):
            dic[key] = getattr(self, key)
        self.builder.connect_signals(dic)
        self.window.show()  # type: ignore
        self.window.show_all()  # type: ignore # Create TextView and use it
        sys.stdout = WritableTextView(
            self.builder.get_object("textview1"))  # type: ignore
        sys.stderr = WritableTextView(
            self.builder.get_object("textview1"),  # type: ignore
            "blue")
        stdlog = WritableTextView(
            self.builder.get_object("textview1"), "red")  # type: ignore
        logging.basicConfig(format="%(module)s: %(message)s", stream=stdlog,
                            level=logging.INFO)
        self.batch_scripts: List[str] = []
        self.batch_tmpdir = ""
        self.batch_target = ""
        self.window.connect("map_event", self.batch_run)

    def _make_sensitive(self, name: str):
        """Set widget called name sensitive."""
        self.builder.get_object(name).set_sensitive(True)  # type: ignore

    def _make_insensitive(self, name: str):
        """Set widget called name insensitive."""
        self.builder.get_object(name).set_sensitive(False)  # type: ignore

    def _is_active(self, name: str) -> bool:
        """Return True if widget "name" is activated, False otherwise."""
        return self.builder.get_object(name).get_active()  # type: ignore

    def set_active(self, name: str):
        """Activate button of widget "name"."""
        self.builder.get_object(name).set_active(1)  # type: ignore

    def set_text(self, name: str, text: str):
        """Set text of widget "name" to text."""
        self.builder.get_object(name).set_text(text)  # type: ignore

    def on_button_open_clicked(self, *dummy: Any):
        """Act as callback for the "open" button."""
        del dummy
        Filechooser1(self.window, self.set_filelist)  # type: ignore

    def on_button_exiimport_browse_importdir_clicked(self, *dummy: Any):
        """Act as callback for the exiimport's "browse importdir" button."""
        del dummy
        Directorychooser1(
            self.window,  # type: ignore
            self.builder.get_object(
                "exiimport_importdir_entry").set_text)  # type: ignore

    def on_button_exiimport_browse_targetdir_clicked(self, *dummy: Any):
        """Act as callback for the exiimport's "browse targetdir" button."""
        del dummy
        Directorychooser1(
            self.window,  # type: ignore
            self.builder.get_object(
                "exiimport_targetdir_entry").set_text)  # type: ignore

    @staticmethod
    def on_info1_activate(*dummy: Any):
        """Act as callback for the "about" menu entry."""
        del dummy
        builder = Gtk.Builder()
        builder.add_objects_from_file(  # type: ignore
            gladefile, ("aboutdialog1",))  # type: ignore
        window = builder.get_object("aboutdialog1")
        window.show_all()  # type: ignore
        window.run()  # type: ignore
        window.hide()  # type: ignore

    @staticmethod
    def on_mainwindow_destroy(*dummy: Any):
        """Act as callback for the window's close button."""
        del dummy
        Gtk.main_quit()

    def set_filelist(self, files: Iterable[str]):
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

    def on_exirename_camid_auto_activate(self, *dummy: Any):
        """Act as callback for exirename's "auto cam_id" selection."""
        del dummy
        self._make_insensitive("exirename_cam_id_entry")

    def on_exirename_camid_custom_activate(self, *dummy: Any):
        """Act as callback for exirename's "custom cam_id" selection."""
        del dummy
        self._make_sensitive("exirename_cam_id_entry")

    def on_exirename_artist_auto_activate(self, *dummy: Any):
        """Act as callback for exirename's "auto artist" selection."""
        del dummy
        self._make_insensitive("exirename_artist_initials_entry")

    def on_exirename_artist_custom_activate(self, *dummy: Any):
        """Act as callback for exirename's "custom artist" selection."""
        del dummy
        self._make_sensitive("exirename_artist_initials_entry")

    def on_exiperson_section_auto_activate(self, *dummy: Any):
        """Act as callback for exirename's "auto section" selection."""
        del dummy
        self._make_insensitive("exiperson_section_entry")

    def on_exiperson_section_custom_activate(self, *dummy: Any):
        """Act as callback for exirename's "custom section" selection."""
        del dummy
        self._make_sensitive("exiperson_section_entry")

    def _progress_callback(self, filename: str, newname: str,
                           percentage: Union[float, int],
                           keep_original: bool = False) -> bool:
        """
        Implement a callback that is given as a callable to the main programs.

        It is called after each processed file. filename and newname may of
        course be the same. If keep_original is True, add newname instead of
        replacing filename with it.
        Return self._cancelled which is True after Cancel has been pressed.
        """
        if filename != newname:
            if keep_original:
                self.liststore.append([newname])
            else:
                for rownum, entry in enumerate(self.liststore):  # type: ignore
                    if entry[0] == filename:
                        self.liststore[rownum][0] = newname
        nbook = self.builder.get_object("notebook1")
        tab = nbook.get_tab_label(  # type: ignore
            nbook.get_nth_page(nbook.get_current_page()))  # type: ignore
        label: str = tab.get_text()  # type: ignore
        progressbar = self.builder.get_object("progressbar1")
        progressbar.set_fraction(float(percentage) / 100)  # type: ignore
        progressbar.set_text(f"{label}:   {percentage} %")  # type: ignore
        while Gtk.events_pending():
            Gtk.main_iteration(False)  # type: ignore
        return self._cancelled

    def on_cancel_activate(self, widget: Gtk.Widget, *dummy: Any):
        """Act as a callback for the cancel button."""
        del dummy
        logger = logging.getLogger("exigui.on_cancel_activate")
        self._cancelled = True
        widget.set_sensitive(False)
        logger.warning("CANCELLED!")

    def on_run_activate(self, widget: Gtk.Widget, *dummy: Any):
        """Act as a callback for the run button."""
        del dummy
        logger = logging.getLogger("exigui.on_run_activate")
        cancel_button = self.builder.get_object("cancel_button")
        cancel_button.set_sensitive(True)  # type: ignore
        nbook = self.builder.get_object("notebook1")
        nbook.set_sensitive(False)  # type: ignore
        widget.set_sensitive(False)
        self._cancelled = False

        tab = nbook.get_tab_label(  # type: ignore
            nbook.get_nth_page(nbook.get_current_page()))  # type: ignore
        label: str = tab.get_text()  # type: ignore
        logger.warning("Running %s", label)
        method = getattr(self, "_run_" + label.replace(" ", "_"))
        method()

        progressbar = self.builder.get_object("progressbar1")
        progressbar.set_fraction(0 / 100)  # type: ignore
        progressbar.set_text("")  # type: ignore
        nbook.set_sensitive(True)  # type: ignore
        cancel_button.set_sensitive(False)  # type: ignore
        widget.set_sensitive(True)

    def _run_exiimport(self):
        """Run exiimport."""
        logger = logging.getLogger("exigui.run_exiimport")
        args = ["-v"]
        import_dir = self.builder.get_object("exiimport_importdir_entry")
        target_dir = self.builder.get_object("exiimport_targetdir_entry")
        if import_dir.get_text():  # type: ignore
            args.append("--mount=" + import_dir.get_text())  # type: ignore
        if target_dir.get_text():  # type: ignore
            args.append("--target=" + target_dir.get_text())  # type: ignore
        try:
            exiimport.run(args, self._progress_callback)
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def _run_exirename(self):
        """Run exirename."""
        logger = logging.getLogger("exigui.run_exirename")
        args = ["-v"]
        initials = self.builder.get_object("exirename_artist_initials_entry")
        cam_id = self.builder.get_object("exirename_cam_id_entry")
        if self._is_active("exirename_artist_initials_entry_button_custom"):
            args.append(
                f"--artist_initials={initials.get_text()}")  # type: ignore
        if self._is_active("exirename_cam_id_entry_button_custom"):
            args.append(f"--cam_id={cam_id.get_text()}")  # type: ignore
        if self._is_active("exirename_include_timestamp_checkbutton"):
            args.append("--with_time")
        args += [entry[0] for entry in self.liststore]
        try:
            exirename.run(args, self._progress_callback)
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def _run_exiperson(self):
        """Run exiperson."""
        logger = logging.getLogger("exigui.run_exiperson")
        args = ["-v"]
        exif_section = self.builder.get_object("exiperson_section_entry")
        if self._is_active("exiperson_section_entry_button_custom"):
            args.append(f"--section={exif_section.get_text()}")  # type: ignore
        args += [entry[0] for entry in self.liststore]
        try:
            exiperson.run(args, self._progress_callback)
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def _run_exiconvert(self):
        """Run exiconvert."""
        logger = logging.getLogger("exigui.run_exiconvert")
        args = ["-v"]
        if self._is_active("exiconvert_remove_lqjpeg_checkbutton"):
            args.append("--remove-lqjpeg")
        args += [entry[0] for entry in self.liststore]
        try:
            exiconvert.run(args, self._progress_callback)
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def _run_exiassign(self):
        """Run exiassign."""
        logger = logging.getLogger("exigui.run_exiassign")
        args = ["-v"]
        if self._is_active("exiassign_force_checkbutton"):
            args.append("--force")
        args += [entry[0] for entry in self.liststore]
        try:
            exiassign.run(args, self._progress_callback)
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def _run_exigate(self):
        """Run exigate."""
        logger = logging.getLogger("exigui.run_exigate")
        args = []
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
        except IOError as msg:
            logger.error("ERROR: %s", msg)

    def batch_run(self, *dummy: Any):
        """Run "scripts" in a batch without user interaction."""
        del dummy
        if len(self.batch_scripts) > 0:
            logger = logging.getLogger("exigui.batch_run")
            nbook = self.builder.get_object("notebook1")
            tabs = []
            for tabnum in range(0, nbook.get_n_pages()):  # type: ignore
                tab_label = nbook.get_tab_label(  # type: ignore
                    nbook.get_nth_page(tabnum))  # type: ignore
                tabs.append(tab_label.get_text())  # type: ignore
            for script in self.batch_scripts:
                if script not in tabs:
                    logger.error("There is no %s tab available!", script)
                    return 1
            run_button = self.builder.get_object("activate_button")
            for script in self.batch_scripts:
                nbook.set_current_page(tabs.index(script))  # type: ignore
                self.on_run_activate(run_button)  # type: ignore
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
                    except shutil.Error as msg:
                        logger.error("ERROR: %s", msg)
                    for rownum, entry in enumerate(  # type: ignore
                            self.liststore):  # type: ignore
                        self.liststore[rownum][0] = \
                            entry[0].replace(  # type: ignore
                                os.path.join(self.batch_tmpdir, subdir),
                                os.path.join(self.batch_target, target_subdir))

        return 0


def run(argv: Sequence[str]):
    """Take an equivalent of sys.argv[1:] and run the GUI."""
    parser = argparse.ArgumentParser()
    parser.set_defaults(batch_order="exiimport,exirename,exiperson,"
                                    "exiconvert,exiassign,exigate")
    parser.add_argument("-m", "--mount", dest="mount",
                        help="Mountpoint of directory to import.")
    parser.add_argument("-t", "--target", dest="target",
                        help="Target directory. A subdirectory will be created"
                        " in this directory.")
    parser.add_argument("-d", "--device", dest="device",
                        help="(Ignored for backwards compatibility. "
                        "Don't use.)")
    parser.add_argument("--cam_id", "-c", dest="cam_id",
                        help="ID string for the camera model. Should normally "
                        "be three characters long.")
    parser.add_argument("--artist_initials", "-a", dest="artist_initials",
                        help="Initials of the artist. Should be two characters"
                        " long.")
    parser.add_argument("-T", "--with_time", action="store_true",
                        dest="with_time",
                        help="Create filenames containing the image time, for"
                        " example 20071231-235959-n001234-xy000.jpg instead"
                        " of 20071231-n001234-xy000.jpg .")
    parser.add_argument("-b", "--batch", action="store_true", dest="batch",
                        help="Autorun from exiimport over exirename, "
                        "exiperson and exiconvert to exiassign.")
    parser.add_argument("--batch_order",
                        help="Comma separated processing order for --batch. "
                        "Default: %default")
    parser.add_argument("--batch_tmpdir",
                        help="If the processing order starts with "
                        "'exiimport', this temporary directory is used for "
                        "batch processing. After batch processing, the "
                        "created subdirectory will be moved into the target "
                        "directory.")
    parser.add_argument("--nofork", action="store_true",
                        help="Do not fork, stay in foreground instead.")
    parser.add_argument("args", nargs="*", metavar="filename",
                        help="An image file")
    options = parser.parse_args(argv)

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
        if len(options.args) > 0:
            win1.set_filelist(options.args)
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

        Gtk.main()

    return 0


if __name__ == "__main__":
    run(sys.argv[1:])
