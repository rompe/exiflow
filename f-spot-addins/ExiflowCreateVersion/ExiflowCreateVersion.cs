/*
 * ExiflowCreateVersion.cs
 *
 * Author(s)
 * 	Sebastian Berthold <exiflow@sleif.de>
 *
 * This is free software. See COPYING for details
 */
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.IO;
using System;
using System.Text.RegularExpressions;
using Gtk;
using Gdk;
using Gnome;
using Gnome.Vfs;

using FSpot;
using FSpot.Extensions;
using Glade;
using Mono.Unix;

//using ExiflowCreateVersionExtension.Extensions;

namespace ExiflowCreateVersionExtension
{
	public class ExiflowCreateVersion: ICommand
	{	
		protected string dialog_name = "exiflow_create_version_dialog";
		protected Glade.XML xml;
		private Gtk.Dialog dialog;

		[Glade.Widget] Gtk.Entry new_version_entry;
		[Glade.Widget] Gtk.Label new_filename_label;
		[Glade.Widget] Gtk.Label overwrite_warning_label;
		[Glade.Widget] Gtk.VBox vbox_combo;
		//[Glade.Widget] Gtk.ComboBox open_with_box;
		[Glade.Widget] Gtk.Button gtk_ok;
		[Glade.Widget] Gtk.CheckButton overwrite_file_ok;
		
		//string new_path;
		//string new_version;


		bool overwrite_file_flag=false;
		string new_filename;
		MimeApplication map = null;
		//bool open;
		Photo currentphoto;
		//string control_file;
		Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-)(.{5}\.[^.]*)$");

		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING DEVELOP IN UFRawExiflow EXTENSION");
			//this.selection = selection;

			
			xml = new Glade.XML (null,"ExiflowCreateVersion.glade", dialog_name, "f-spot");
			xml.Autoconnect (this);
			dialog = (Gtk.Dialog) xml.GetWidget(dialog_name);
			foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				this.currentphoto = p;
				//Console.WriteLine ("MimeType: "+ MainWindow.Toplevel.SelectedMimeTypes);
				Console.WriteLine ("MimeType: "+ Gnome.Vfs.MimeType.GetMimeTypeForUri (p.DefaultVersionUri.ToString ()));
				
				PhotoVersion raw = p.GetVersion (Photo.OriginalVersionId) as PhotoVersion;
				//if (!ImageFile.IsRaw (raw.Uri.AbsolutePath)) {
				//	Console.WriteLine ("The Original version of this image is not a (supported) RAW file");
				//	continue;
				//}
				uint default_id = p.DefaultVersionId;
				Console.WriteLine ("DefaultVersionId: "+default_id);
				string filename = GetNextVersionFileName (p);
				System.Uri developed = GetUriForVersionFileName (p, filename);
			//new_filename_entry.Text = filename;
				new_version_entry.Text = GetVersionName(filename);
				//open_with_box.AppendText("gimp-remoteyyy");
				ComboBox owcb = GetComboBox ();
				//Console.WriteLine ("\n\n\nAppending gimp-remotexxx\n");
				//owcb.AppendText("gimp-remotexxx");
				//Console.WriteLine ("Appended gimp-remotexxx\n\n\n");
				vbox_combo.PackStart (owcb, false, true, 0);
				string args = String.Format("--exif --overwrite --compression=95 --out-type=jpeg --output={0} {1}", 
					CheapEscape (developed.LocalPath),
					CheapEscape (raw.Uri.ToString()));
				Console.WriteLine ("ufraw "+args);

				dialog.Modal = false;
				dialog.TransientFor = null;
			
				dialog.Response += HandleResponse;

			}	
			dialog.ShowAll();
		}

		private OpenWithComboBox owcb;

		public Gtk.ComboBox GetComboBox ()
		{
			System.Console.WriteLine ("Hallo 1");
			owcb = new OpenWithComboBox (MainWindow.Toplevel.SelectedMimeTypes);
			owcb.IgnoreApp = "f-spot";
			//owcb.ApplicationActivated += delegate (Gnome.Vfs.MimeApplication app) { MainWindow.Toplevel.HandleOpenWith (this, app); };
                        if (owcb != null)
                        	owcb.Populate ();

			return owcb;
		}

		private void HandleResponse (object sender, Gtk.ResponseArgs args)
		{
			if (args.ResponseId != Gtk.ResponseType.Ok) {
				// FIXME this is to work around a bug in gtk+ where
				// the filesystem events are still listened to when
				// a FileChooserButton is destroyed but not finalized
				// and an event comes in that wants to update the child widgets.
				dialog.Destroy ();
			Console.WriteLine ("cancel pressed");
				//uri_chooser.Dispose ();
				//uri_chooser = null;
				return;
			}
			
			Console.WriteLine ("ok pressed in DEVELOP IN UFRawExiflow EXTENSION");
			//new_version = new_version_entry.Text;
			new_filename = new_filename_label.Text;
			//open = open_check.Active;
			
			//command_thread = new System.Threading.Thread (new System.Threading.ThreadStart (CreateSlideshow));
			//command_thread.Name = Catalog.GetString ("Creating Slideshow");

			//progress_dialog = new FSpot.ThreadProgressDialog (command_thread, 1);
			//progress_dialog.Start ();
			CreateNewVersion();

		}

		protected void CreateNewVersion()
		{
			try {
				System.Uri original_uri = GetUriForVersionFileName (this.currentphoto, this.currentphoto.DefaultVersionUri.LocalPath);
				System.Uri new_uri = GetUriForVersionFileName (this.currentphoto, new_filename);
				Console.WriteLine ("ok pressed: old: " + this.currentphoto.DefaultVersionUri.LocalPath + "; " + original_uri.ToString() + " new: " + new_filename + "; " + new_uri.ToString() + "to open with: " );
				Xfer.XferUri (
					new Gnome.Vfs.Uri (original_uri.ToString ()), 
					new Gnome.Vfs.Uri (new_uri.ToString ()),
					XferOptions.Default, XferErrorMode.Abort, 
					XferOverwriteMode.Abort, 
					delegate (Gnome.Vfs.XferProgressInfo info) {return 1;});
				FSpot.ThumbnailGenerator.Create (new_uri).Dispose ();
				this.currentphoto.DefaultVersionId = this.currentphoto.AddVersion (new_uri, new_version_entry.Text, true);
				Core.Database.Photos.Commit (this.currentphoto);

				MainWindow.Toplevel.Query.MarkChanged(MainWindow.Toplevel.Query.IndexOf(this.currentphoto));

				Gtk.TreeIter iter;
			        if (owcb.GetActiveIter (out iter)){
			                //Console.WriteLine ((string) owcb.Model.GetValue (iter, 0));
			                //Console.WriteLine ((string) owcb.Model.GetValue (iter, 1));
					//Console.WriteLine ("Getting applications again");
			
					ArrayList union = new ArrayList();	
					foreach (string mime_type in (string []) owcb.Model.GetValue (iter, 2)) {
						if (mime_type == null)
							continue;
						MimeApplication [] apps = Gnome.Vfs.Mime.GetAllApplications (mime_type);
						foreach (MimeApplication app in apps) {
							if (! union.Contains (app))
								union.Add (app);
						}
					}
					foreach (MimeApplication app in union) {
						if (app.BinaryName.ToString() == (string) owcb.Model.GetValue (iter, 1)){
			                		//Console.WriteLine ("Winner is "+ (string) owcb.Model.GetValue (iter, 1));
							// is there a better way to get a GLib.List???
							GLib.List uri_list = new GLib.List (typeof (string));
							uri_list.Append(new_uri.ToString());
							app.Launch (uri_list);
						}
					}	
				}
			} finally {
				Gtk.Application.Invoke (delegate { dialog.Destroy(); });
			}
		}
		
		private void on_new_version_entry_changed(object o, EventArgs args)
		{
			Console.WriteLine ("changed filename with: " + new_version_entry.Text);
			new_filename_label.Text = GetFilenameDateAndNumberPart(this.currentphoto.Name) + new_version_entry.Text;
			if ((FileExist(this.currentphoto, new_filename_label.Text)) || 
				(! IsExiflowSchema(new_filename_label.Text)) ||
				(VersionExist(this.currentphoto, new_version_entry.Text))
				)
			{
				gtk_ok.Sensitive=false;
			}
			else
			{
				overwrite_warning_label.Text = String.Empty;
				gtk_ok.Sensitive=true;
				overwrite_file_ok.Sensitive=false;
				overwrite_file_ok.Active=false;
			}		

			if (VersionExist(this.currentphoto, new_version_entry.Text))
			{
				Console.WriteLine ("version exists " + new_version_entry.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting version already exists!</small></span>";
				overwrite_file_ok.Sensitive=true;
			}
			if (FileExist(this.currentphoto, new_filename_label.Text))
			{
				Console.WriteLine ("filename exists " + new_filename_label.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting file already exists!</small></span>";
				overwrite_file_ok.Sensitive=true;
			}
			else 
			{
				//overwrite_warning_label.Text = "";
				//overwrite_file_ok.Sensitive=false;
				//overwrite_file_ok.Active=false;
			}
			if ((FileExist(this.currentphoto, new_filename_label.Text)) &&
				(VersionExist(this.currentphoto, new_version_entry.Text))
				)
			{
				Console.WriteLine ("file and version exists " + new_version_entry.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting file and version already exists!</small></span>";
				overwrite_file_ok.Sensitive=true;
			}


			if (! IsExiflowSchema(new_filename_label.Text))
			{
				Console.WriteLine ("not in exiflow schema " + new_filename_label.Text);
				overwrite_warning_label.Markup = "<span foreground='red'>Error: resulting filename is not in the exiflow schema!</span>";
//				overwrite_warning_label.Text = "Error: new filename is not in the exiflow schema!";
				overwrite_file_ok.Sensitive=false;
				overwrite_file_ok.Active=false;
			}
			else 
			{
				//overwrite_warning_label.Text = "";
			}

		}

		private void on_overwrite_file_ok_toggled(object o , EventArgs args)
		{
			if (overwrite_file_ok.Active == true )
			{
				gtk_ok.Sensitive=true;
				overwrite_file_flag=true;
			}
			else
			{
				overwrite_file_ok.Sensitive=false;
				on_new_version_entry_changed(null,null);
				overwrite_file_flag=false;
			}
				
		}

		//private string CreateExiflowFilenameForVersion(Photo p , string newversion)
		//{
		//		Console.WriteLine ("exiflow");
		//		return p.Name;
		//	
		//}
      	

		private bool IsExiflowSchema(string filename)
		{
			Regex exiflowpat = new Regex(@"^\d{8}(-\d{6})?-.{3}\d{4}-.{2}\d.{2}\.[^.]*$");
			if (exiflowpat.IsMatch(filename))
			{
				Console.WriteLine ("exiflow ok " + filename);
				return true;
			}
			else
			{
				Console.WriteLine ("exiflow not ok " + filename);
				return false;
			}
		}

		private bool VersionExist(Photo p, string newversionname)
		{
			if (p.VersionNameExists(newversionname))
				return true;
			return false;
		}

		private bool FileExist(Photo p, string newfilename)
		{
			System.Uri filenameuri = GetUriForVersionFileName (p, newfilename);
			if (System.IO.File.Exists(CheapEscape(filenameuri.LocalPath)))
				return true;
			return false;
			
		}

//		private static NextInExiflowSchema(string filename)
//		{
//			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(\d)(.{2}\.[^.]*$)");
//			Match exiflowpatmatch = exiflowpat.Match(filename);
//			string filename = String.Format("{0}{1}00.jpg", exiflowpatmatch.Groups[1], i);
//			System.Uri developed = GetUriForVersionFileName (p, filename);
//			if (p.VersionNameExists (GetVersionName(filename)) || File.Exists(CheapEscape(developed.LocalPath)))
//				return GetNextVersionFileName (p, i + 1);
//			return filename;
//			
//		}

		private static string GetNextVersionFileName (Photo p)
		{
			return GetNextVersionFileName (p, 0);
		}

		private static string GetNextVersionFileName (Photo p, int i)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(\d)(.{2})\.([^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(System.IO.Path.GetFileName(p.VersionUri(p.DefaultVersionId).LocalPath));
// besser mit UnixPath.GetFileName()
			string filename = String.Format("{0}{1}00.{2}", exiflowpatmatch.Groups[1], i, exiflowpatmatch.Groups[5]);
			System.Uri developed = GetUriForVersionFileName (p, filename);
			if (p.VersionNameExists (GetVersionName(filename)) || System.IO.File.Exists(CheapEscape(developed.LocalPath)))
				return GetNextVersionFileName (p, i + 1);
			return filename;
		}

		private static string GetVersionName (string filename)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-)(.{5}\.[^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(filename);
			string versionname = String.Format("{0}", exiflowpatmatch.Groups[3]);
			return versionname;
		}

		private string GetFilenameDateAndNumberPart (string filename)
		{
			//Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-)(.{5}\.[^.]*)$");
			Match exiflowpatmatch = this.exiflowpat.Match(filename);
			string datenumber = String.Format("{0}", exiflowpatmatch.Groups[1]);
			return datenumber;
		}

		private static System.Uri GetUriForVersionFileName (Photo p, string version_name)
		{
			return new System.Uri (System.IO.Path.Combine (DirectoryPath (p),  version_name ));
		}

		private static string CheapEscape (string input)
		{
			string escaped = input;
			escaped = escaped.Replace (" ", "\\ ");
			escaped = escaped.Replace ("(", "\\(");
			escaped = escaped.Replace (")", "\\)");
			return escaped;
		}
		
		private static string DirectoryPath (Photo p)
		{
			System.Uri uri = p.VersionUri (Photo.OriginalVersionId);
			return uri.Scheme + "://" + uri.Host + System.IO.Path.GetDirectoryName (uri.AbsolutePath);
		}
	}







  






	public class OpenWithComboBox: Gtk.ComboBox {
		//public delegate void OpenWithHandler (MimeApplication app);
		//public event OpenWithHandler ApplicationActivated;
	

		public delegate string [] MimeFetcher ();
		private MimeFetcher mime_fetcher;
	
		private string [] mime_types;
		private bool populated = false;
		
		private string ignore_app = null;
		public string IgnoreApp {
			get { return ignore_app; }
			set { ignore_app = value; }
		}
	
		private bool show_icons = false;
		public bool ShowIcons {
			get { return show_icons; }
			set { show_icons = value; }
		}
	
		private bool hide_invalid = true;
		public bool HideInvalid {
			get { return hide_invalid; }
			set { hide_invalid = value; }
		}
	
		//static OpenWithComboBox () {
		//	Gnome.Vfs.Vfs.Initialize ();
		//}
	
		public OpenWithComboBox (MimeFetcher mime_fetcher)
		{
			this.mime_fetcher = mime_fetcher;
		}
		
		public void Populate ()
		{
			this.Clear();
			CellRendererText cell = new CellRendererText();
			this.PackStart(cell, false);
			this.AddAttribute(cell, "text", 0);
			TreeStore store = new Gtk.TreeStore(typeof (string), typeof (string), typeof (string[]));
			this.Model = store;

			string [] mime_types = mime_fetcher ();
	
			foreach (string mime in mime_types)
				System.Console.WriteLine ("Populating open with menu for {0}", mime);
			
			if (this.mime_types != mime_types && populated) {
				populated = false;
	
				Widget [] dead_pool = Children;
				for (int i = 0; i < dead_pool.Length; i++)
					dead_pool [i].Destroy ();
			}
	
			if (populated)
				return;
	
			ArrayList union, intersection;
			ApplicationsFor (this, mime_types, out union, out intersection);
	
			ArrayList list = (HideInvalid) ? intersection : union;

			//ExiflowCreateVersionExtension.ExiflowCreateVersion.map = list[2];	
			//System.Console.WriteLine ("Adding mmmmmmapp {0} to open with combo box (binary name = {1})", ExiflowCreateVersionExtension.ExiflowCreateVersion.map.Name, ExiflowCreateVersionExtension.ExiflowCreateVersion.map.BinaryName);
			store.AppendValues("", "", mime_types);
			foreach (MimeApplication app in list) {
				System.Console.WriteLine ("Adding app {0} to open with combo box (binary name = {1})", app.Name, app.BinaryName);
				//System.Console.WriteLine ("Desktop file path: {0}, id : {1}", app.DesktopFilePath);
				//this.AppendText(app.BinaryName.ToString());
				//store.AppendValues(app.BinaryName.ToString());
				//store.AppendValues(app.BinaryName.ToString(), ExiflowCreateVersionExtension.ExiflowCreateVersion.map);
				store.AppendValues(app.Name.ToString(), app.BinaryName.ToString(), mime_types);
				//this.InsertText(2, "ggimp");
			}
			// empty field to reset combo box
			//store.AppendValues("");
	
			populated = true;
		}
	
		private static void ApplicationsFor (OpenWithComboBox owcb, string [] mime_types, out ArrayList union, out ArrayList intersection)
		{
			Console.WriteLine ("Getting applications");
			union = new ArrayList ();
			intersection = new ArrayList ();
			
			if (mime_types == null || mime_types.Length < 1)
				return;
	
			bool first = true;
			foreach (string mime_type in mime_types) {
				if (mime_type == null)
					continue;
	
				MimeApplication [] apps = Gnome.Vfs.Mime.GetAllApplications (mime_type);
				for (int i = 0; i < apps.Length; i++) {
					apps [i] = apps [i].Copy ();
				}
	
			Console.WriteLine ("Disable " + owcb.IgnoreApp);
				foreach (MimeApplication app in apps) {
					// Skip apps that don't take URIs
					if (! app.SupportsUris ())
						continue;
					
					// Skip apps that we were told to ignore
					if (owcb.IgnoreApp != null)
						if (app.BinaryName.IndexOf (owcb.IgnoreApp) != -1)
							continue;
	
					if (! union.Contains (app))
						union.Add (app);
					
					if (first)
						intersection.Add (app);
				}
	
				if (! first) {
					for (int i = 0; i < intersection.Count; i++) {
						MimeApplication app = intersection [i] as MimeApplication;
						if (System.Array.IndexOf (apps, app) == -1) {
							intersection.Remove (app);
							i--;
						}
					}
				}
	
				first = false;
			}
		}
		
		//private void HandleItemActivated (object sender, EventArgs args)
		//{
		//	AppMenuItem app = (sender as AppMenuItem);
		//
		//	if (ApplicationActivated != null)
		//		ApplicationActivated (app.App);
		//}
		
	}
}
