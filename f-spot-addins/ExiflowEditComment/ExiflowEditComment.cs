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


		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING ExiflowEditComment EXTENSION");
			
			xml = new Glade.XML (null,"ExiflowEditComment.glade", dialog_name, "f-spot");
			xml.Autoconnect (this);
			dialog = (Gtk.Dialog) xml.GetWidget(dialog_name);
			
			ArrayList current_comments = new ArrayList ();

			foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				// Todo: get existing comment and append to current_comments
				current_comments.Add(p.Name + p.Description);
			}
			
			// Todo: show dialog filled with joined current_comments
			//comment.Buffer.Text = "blafasel";
			comment.Buffer.Text = String.Join(" und ", (String[]) current_comments.ToArray(typeof(string)));

			dialog.Modal = false;
			dialog.TransientFor = null;
			dialog.Response += HandleResponse;
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
			Console.WriteLine ("ok pressed in ExiflowEditComments EXTENSION");
			Console.WriteLine ("New comment is: " + comment.Buffer.Text);
			foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				p.Description = comment.Buffer.Text;
				MainWindow.Toplevel.Query.MarkChanged(MainWindow.Toplevel.Query.IndexOf(p));
				Core.Database.Photos.Commit (p);
			}
			dialog.Destroy ();
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
