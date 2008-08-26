/*
 * ExiflowRenameVersion.cs
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
using Gnome;
using Gnome.Vfs;

using FSpot;
using FSpot.Extensions;
using Mono.Unix;

namespace ExiflowRenameVersionExtension
{
	public class ExiflowRenameVersion: ICommand
	{	
		protected string dialog_name = "exiflow_rename_version_dialog";
		private Gtk.Dialog dialog;

		Gtk.RadioButton versionrb = new Gtk.RadioButton("");
		Gtk.Label new_filename_label = new Gtk.Label("");
		Gtk.Label overwrite_warning_label = new Gtk.Label("");
		Gtk.Entry new_version_entry = new Gtk.Entry("");
		Gtk.CheckButton overwrite_file_ok = new Gtk.CheckButton("_Overwrite existing file");
		Gtk.Button gtk_cancel = new Gtk.Button("gtk-cancel");
		Gtk.Button gtk_ok = new Gtk.Button("gtk-ok");

		string new_filename;
		Photo currentphoto;
		Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-)(.{5}\.[^.]*)$");

		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING ExiflowRenameVersion EXTENSION");
			
			Window win = new Window ("window");
			dialog = new Dialog (dialog_name, win, Gtk.DialogFlags.DestroyWithParent);

			Frame frame_versions = new Frame ("new version");
			HBox hbox_versions = new HBox();
			frame_versions.Child = hbox_versions;

				// RadioButtons left
				VBox vbox_versions_left = new VBox ();
				hbox_versions.PackStart (vbox_versions_left, true, false, 0);
				// EntryBox right
				VBox vbox_versions_right = new VBox ();
				hbox_versions.PackStart (vbox_versions_right, true, false, 0);
				vbox_versions_right.PackStart (new_version_entry, true, false, 0);
				vbox_versions_right.PackStart (overwrite_file_ok, true, false, 0);

			Frame frame_resulting_filename = new Frame ("resulting filename");
			VBox vbox_resulting_filename = new VBox ();
			frame_resulting_filename.Child = vbox_resulting_filename;
				vbox_resulting_filename.PackStart (new_filename_label, true, false, 0);
				vbox_resulting_filename.PackStart (overwrite_warning_label, true, false, 0);
			
			new_version_entry.Changed += new EventHandler (on_new_version_entry_changed);
			overwrite_file_ok.Toggled += new EventHandler (on_overwrite_file_ok_toggled);

			gtk_cancel.UseStock = true;
			gtk_cancel.Clicked += CancelClicked;
			gtk_ok.UseStock = true;
			gtk_ok.Clicked += OkClicked;

			foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				this.currentphoto = p;
				//Console.WriteLine ("MimeType: "+ Gnome.Vfs.MimeType.GetMimeTypeForUri (p.DefaultVersionUri.ToString ()));
				
				//uint default_id = p.DefaultVersionId;
				//Console.WriteLine ("DefaultVersionId: "+default_id);
				//string filename = GetNextIntelligentVersionFileNames (p)[0];

				string [] possiblefilenames = GetNextIntelligentVersionFileNames(p);
				new_version_entry.Text = GetVersionName(possiblefilenames[0].ToString());

				for (int i=0; i < possiblefilenames.Length; i++ ){
					Gtk.RadioButton rb = new Gtk.RadioButton (versionrb,GetVersionName(possiblefilenames[i].ToString()));
					rb.Clicked += new EventHandler(on_versionrb_changed);
					vbox_versions_left.PackStart (rb, true, false, 0);
					
				}

				dialog.Modal = false;
				dialog.TransientFor = null;
			}	

			VBox vbox_main = new VBox ();
				vbox_main.PackStart (frame_versions);
				vbox_main.PackStart (frame_resulting_filename);

			HButtonBox hbb_ok_cancel = new HButtonBox ();
				hbb_ok_cancel.PackStart (gtk_cancel, true, false, 0);
				hbb_ok_cancel.PackStart (gtk_ok, true, false, 0);

			dialog.VBox.PackStart(vbox_main, false, true,0);
			dialog.ActionArea.PackStart (hbb_ok_cancel, false,true,0);
			dialog.ShowAll();
		}

		private void CancelClicked (object sender, EventArgs args)
		{
			dialog.Destroy ();
			//Console.WriteLine ("cancel pressed");
			return;
		}

		private void OkClicked (object sender, EventArgs args)
		{
			//Console.WriteLine ("ok pressed");
			new_filename = new_filename_label.Text;
			RenameNewVersion();
		}

		protected void RenameNewVersion()
		{
			try {
				System.Uri original_uri = GetUriForVersionFileName (this.currentphoto, this.currentphoto.DefaultVersionUri.LocalPath);
				System.Uri new_uri = GetUriForVersionFileName (this.currentphoto, new_filename);
				//Console.WriteLine ("ok pressed: old: " + this.currentphoto.DefaultVersionUri.LocalPath + "; " + original_uri.ToString() + " new: " + new_filename + "; " + new_uri.ToString() + "to open with: " );

                                // check if new version exist and remove
                                foreach (uint id in currentphoto.VersionIds) {
					if ( currentphoto.GetVersion (id).Name == new_version_entry.Text ) {
						this.currentphoto.DeleteVersion ( id );
					}
				}
				Xfer.XferUri (
					new Gnome.Vfs.Uri (original_uri.ToString ()), 
					new Gnome.Vfs.Uri (new_uri.ToString ()),
					XferOptions.Default, XferErrorMode.Abort, 
					XferOverwriteMode.Abort, 
					delegate (Gnome.Vfs.XferProgressInfo info) {return 1;});
				FSpot.ThumbnailGenerator.Create (new_uri).Dispose ();
				this.currentphoto.DefaultVersionId = this.currentphoto.AddVersion (new_uri, new_version_entry.Text, true);
				uint currentid = this.currentphoto.DefaultVersionId;
				foreach (uint id in currentphoto.VersionIds){
					if ( currentphoto.GetVersion (id).DefaultVersionUri.ToString() == original_uri.ToString() ) {
						this.currentphoto.DeleteVersion (id, false, false);
					}
				}
				this.currentphoto.DefaultVersionId = currentid;
				Core.Database.Photos.Commit (this.currentphoto);

				this.currentphoto.Changes.DataChanged = true;
			} finally {
				Gtk.Application.Invoke (delegate { dialog.Destroy(); });
			}
		}
		
		private void on_versionrb_changed(object o, EventArgs args)
		{
			foreach (RadioButton rb in versionrb.Group) {
				if (rb.Active) new_version_entry.Text = rb.Label;
			}
		}
		private void on_new_version_entry_changed(object o, EventArgs args)
		{
			//Console.WriteLine ("changed filename with: " + new_version_entry.Text);
			new_filename_label.Text = GetFilenameDateAndNumberPart(this.currentphoto.Name) + new_version_entry.Text;
			if ((FileExist(this.currentphoto, new_filename_label.Text)) || 
				(! IsExiflowSchema(new_filename_label.Text)) ||
				(this.currentphoto.VersionNameExists( new_version_entry.Text ))
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

			if (this.currentphoto.VersionNameExists( new_version_entry.Text ))
			{
				//Console.WriteLine ("version exists " + new_version_entry.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting version already exists!</small></span>";
				overwrite_file_ok.Label = "_Overwrite existing version!";
				overwrite_file_ok.Sensitive=true;
			}
			if (FileExist(this.currentphoto, new_filename_label.Text))
			{
				//Console.WriteLine ("filename exists " + new_filename_label.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting file already exists!</small></span>";
				overwrite_file_ok.Label = "_Overwrite existing file!";
				overwrite_file_ok.Sensitive=true;
			}

			if ((FileExist(this.currentphoto, new_filename_label.Text)) &&
				(this.currentphoto.VersionNameExists(new_version_entry.Text))
				)
			{
				//Console.WriteLine ("file and version exists " + new_version_entry.Text);
				overwrite_warning_label.Markup = "<span foreground='blue'><small>Warning: resulting file and version already exists!</small></span>";
				overwrite_file_ok.Label = "_Overwrite existing file and version!";
				overwrite_file_ok.Sensitive=true;
			}

			if ( currentphoto.GetVersion (currentphoto.DefaultVersionId).Name == new_version_entry.Text ) {
				overwrite_warning_label.Markup = "<span foreground='red'>Error: New version name must be different from original!</span>";
				overwrite_file_ok.Label = "_Overwriting not allowed!";
				overwrite_file_ok.Sensitive=false;
				overwrite_file_ok.Active=false;
			}

			if (! IsExiflowSchema(new_filename_label.Text))
			{
				//Console.WriteLine ("not in exiflow schema " + new_filename_label.Text);
				overwrite_warning_label.Markup = "<span foreground='red'>Error: resulting filename is not in the exiflow schema!</span>";
				overwrite_file_ok.Label = "New version must fit the exiflow schema!";
				overwrite_file_ok.Sensitive=false;
				overwrite_file_ok.Active=false;
			}
		}

		private void on_overwrite_file_ok_toggled(object o , EventArgs args)
		{
			if (overwrite_file_ok.Active == true )
			{
				gtk_ok.Sensitive=true;
			}
			else
			{
				overwrite_file_ok.Sensitive=false;
				on_new_version_entry_changed(null,null);
			}
				
		}

		private bool IsExiflowSchema(string filename)
		{
			Regex exiflowpat = new Regex(@"^\d{8}(-\d{6})?-.{3}\d{4}-.{2}.{3}\.[^.]*$");
			if (exiflowpat.IsMatch(filename))
			{
				//Console.WriteLine ("exiflow ok " + filename);
				return true;
			}
			else
			{
				//Console.WriteLine ("exiflow not ok " + filename);
				return false;
			}
		}

		private bool FileExist(Photo p, string newfilename)
		{
			System.Uri filenameuri = GetUriForVersionFileName (p, newfilename);
			if (System.IO.File.Exists(CheapEscape(filenameuri.LocalPath)))
				return true;
			return false;
			
		}

		private static string GetNextVersionFileName (Photo p, int i)
		{
				Console.WriteLine ("New New "+ GetNextIntelligentVersionFileNames(p)[0].ToString());
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(\d)(.{2})\.([^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(System.IO.Path.GetFileName(p.VersionUri(p.DefaultVersionId).LocalPath));
// besser mit UnixPath.GetFileName()
			string filename = String.Format("{0}{1}00.{2}", exiflowpatmatch.Groups[1], i, exiflowpatmatch.Groups[5]);
			System.Uri developed = GetUriForVersionFileName (p, filename);
			if (p.VersionNameExists (GetVersionName(filename)) || System.IO.File.Exists(CheapEscape(developed.LocalPath)))
				return GetNextVersionFileName (p, i + 1);
			return filename;
		}

		private static string [] GetNextIntelligentVersionFileNames (Photo p)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(\d)(.)(.)(.*)\.([^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(System.IO.Path.GetFileName(p.VersionUri(p.DefaultVersionId).LocalPath));
			if ( (exiflowpatmatch.Groups[3].ToString() == "0") && 
			      (exiflowpatmatch.Groups[4].ToString() == "0") && 
			      (exiflowpatmatch.Groups[5].ToString() == "0" )) {
				string [] possibleversions = { GetNextIntelligentVersionFileNames (p, 1, 0 , 0)};
				return possibleversions;
			}
			else if ( (exiflowpatmatch.Groups[3].ToString() != "0") && 
			      (exiflowpatmatch.Groups[4].ToString() == "0") && 
			      (exiflowpatmatch.Groups[5].ToString() == "0" )) {
				string [] possibleversions = { 
				  GetNextIntelligentVersionFileNames (p, 0, 1, 0),
				  GetNextIntelligentVersionFileNames (p, 1, 0, 0)
				};
				return possibleversions;
			}
			else
			{
				string [] possibleversions = { 
				  GetNextIntelligentVersionFileNames (p, 0, 0, 1),
				  GetNextIntelligentVersionFileNames (p, 0, 1, 0),
				  GetNextIntelligentVersionFileNames (p, 1, 0, 0)
				};
				return possibleversions;
			}
		}

		private static string GetNextIntelligentVersionFileNames (Photo p, int x, int y, int z)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}(-\d{6})?-.{3}\d{4}-.{2})(.)(.)(.)(.*)\.([^.]*)$");
			Match exiflowpatmatch = exiflowpat.Match(System.IO.Path.GetFileName(p.VersionUri(p.DefaultVersionId).LocalPath));
			string filename = null;	
			if (x > 0)
				filename = String.Format("{0}{1}{2}{3}.{4}",
				 exiflowpatmatch.Groups[1], 
				 GetNextValidChar(exiflowpatmatch.Groups[3].ToString(),x),
				 0,
				 0,
				 exiflowpatmatch.Groups[7]);
			if (y > 0)
				filename = String.Format("{0}{1}{2}{3}.{4}",
				 exiflowpatmatch.Groups[1], 
				 exiflowpatmatch.Groups[3],
				 GetNextValidChar(exiflowpatmatch.Groups[4].ToString(),y),
				 0,
				 exiflowpatmatch.Groups[7]);
			if (z > 0)
				filename = String.Format("{0}{1}{2}{3}.{4}",
				 exiflowpatmatch.Groups[1], 
				 exiflowpatmatch.Groups[3], 
				 exiflowpatmatch.Groups[4], 
				 GetNextValidChar(exiflowpatmatch.Groups[5].ToString(),z),
				 exiflowpatmatch.Groups[7]);
			System.Uri developed = GetUriForVersionFileName (p, filename);
				Console.WriteLine (developed);
			if (p.VersionNameExists (GetVersionName(filename)) || System.IO.File.Exists(CheapEscape(developed.LocalPath))){
				if (x > 0)
					return GetNextIntelligentVersionFileNames (p, x+1, y, z);
				if (y > 0)
					return GetNextIntelligentVersionFileNames (p, x, y+1, z);
				if (z > 0)
					return GetNextIntelligentVersionFileNames (p, x, y, z+1);
			}
			return filename;
		}
		
		private static string GetNextValidChar (string s, int i)
		{
			string validchars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
			if (validchars.IndexOf(s[0]) + i < validchars.Length){
				return validchars[validchars.IndexOf(s[0]) + i].ToString();
			}
			else {
				return null;
			}
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
}
