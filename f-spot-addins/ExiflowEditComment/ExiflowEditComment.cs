/*
 * ExiflowEditComment.cs
 *
 * Author(s)
 * 	Ulf Rompe <f-spot.org@rompe.org>
 *
 * This is free software. See COPYING for details
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

using FSpot;
using FSpot.Extensions;
using Glade;
using Mono.Unix;

namespace ExiflowEditCommentExtension
{
	public class ExiflowEditComment: ICommand
	{	
		//IBrowsableCollection selection;

		protected string dialog_name = "exiflow_edit_comment_dialog";
		protected Glade.XML xml;
		private Gtk.Dialog dialog;

		[Glade.Widget] Gtk.TextView comment;

		FSpot.ThreadProgressDialog progress_dialog;
		System.Threading.Thread command_thread;
		
		string new_path;
		string new_version;
		string new_filename;
		bool open;
		
		string control_file;

		//public void Run (IBrowsableCollection selection)
		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING DEVELOP IN UFRawExiflow EXTENSION");
			//this.selection = selection;

			
			xml = new Glade.XML (null,"ExiflowEditComment.glade", dialog_name, "f-spot");
			xml.Autoconnect (this);
			dialog = (Gtk.Dialog) xml.GetWidget(dialog_name);
				
		foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				PhotoVersion raw = p.GetVersion (Photo.OriginalVersionId) as PhotoVersion;
				//if (!ImageFile.IsRaw (raw.Uri.AbsolutePath)) {
				//	Console.WriteLine ("The Original version of this image is not a (supported) RAW file");
				//	continue;
				//}

				string filename = GetVersionFileName (p);
				System.Uri developed = GetUriForVersionFileName (p, filename);
			//new_filename_entry.Text = filename;
			new_version_entry.Text = GetVersionName(filename);
				string args = String.Format("--exif --overwrite --compression=95 --out-type=jpeg --output={0} {1}", 
					CheapEscape (developed.LocalPath),
					CheapEscape (raw.Uri.ToString()));
				Console.WriteLine ("ufraw "+args);

				//System.Diagnostics.Process ufraw = System.Diagnostics.Process.Start ("ufraw", args); 
				//ufraw.WaitForExit ();
				//if (!(new Gnome.Vfs.Uri (developed.ToString ())).Exists) {
				//	Console.WriteLine ("UFraw didn't ended well. Check that you have UFRaw 0.13 (or CVS newer than 2007-09-06). Or did you simply clicked on Cancel ?");
				//	continue;
				//}

				//p.DefaultVersionId = p.AddVersion (developed, GetVersionName(filename), true);
				//Core.Database.Photos.Commit (p);

			dialog.Modal = false;
			dialog.TransientFor = null;
			
			dialog.Response += HandleResponse;

			//thumb_scrolledwindow.Add (view);
			}	
		dialog.ShowAll();
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
			new_version = new_version_entry.Text;
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
				Console.WriteLine ("ok pressed: filename: " + new_filename);
			} finally {
				Gtk.Application.Invoke (delegate { dialog.Destroy(); });
			}
		}
		
		private void on_new_version_entry_changed(object o, EventArgs args)
		{
			Console.WriteLine ("changed filename mit: " + new_version_entry.Text);
			new_filename_label.Text = new_version_entry.Text;
		}

		//private void CreateExiflowFilenameForVersion(string filenamesrc, string version)
		private void CreateExiflowFilenameForVersion(Photo p , string newversion)
		{
				Console.WriteLine ("exiflow");
				return ;
			
		}
      	

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

		private bool VersionExist(Photo p, string newfilename)
		{
			if (p.VersionNameExists(GetVersionName(newfilename)))
				return true;
			return false;
			
		}

		private bool FileExist(Photo p, string newfilename)
		{
			System.Uri filenameuri = GetUriForVersionFileName (p, newfilename);
			if (File.Exists(CheapEscape(filenameuri.LocalPath)))
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
//				return GetVersionFileName (p, i + 1);
//			return filename;
//			
//		}

		private static string GetVersionFileName (Photo p)
		{
			return GetVersionFileName (p, 0);
		}

		private static string GetVersionFileName (Photo p, int i)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(\d)(.{2}\.[^.]*$)");
			Match exiflowpatmatch = exiflowpat.Match(p.Name);
			string filename = String.Format("{0}{1}00.jpg", exiflowpatmatch.Groups[1], i);
			System.Uri developed = GetUriForVersionFileName (p, filename);
			if (p.VersionNameExists (GetVersionName(filename)) || File.Exists(CheapEscape(developed.LocalPath)))
				return GetVersionFileName (p, i + 1);
			return filename;
		}

		private static string GetVersionName (string filename)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-)(.{5}\.[^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(filename);
			string versionname = String.Format("{0}", exiflowpatmatch.Groups[3]);
			return versionname;
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
}
