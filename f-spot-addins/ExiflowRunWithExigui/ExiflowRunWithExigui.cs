/*
 * ExiflowRunWithExigui.cs
 *
 * Author(s)
 * 	Sebastian Berthold <exiflow@sleif.de>
 *
 * This is free software. See COPYING for details
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;

using Gtk;

using FSpot;
using FSpot.UI.Dialog;
using FSpot.Extensions;

namespace ExiflowRunWithExiguiExtension
{
	public class ExiflowRunWithExigui : ICommand
	{
		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING ExiflowRunWithExigui Extension");

			string filelist = "";
			
			foreach (Photo p in App.Instance.Organizer.SelectedPhotos ()) {
				foreach (uint version_id in p.VersionIds) {
					PhotoVersion pv = p.GetVersion (version_id) as PhotoVersion;
					filelist = filelist + " " + CheapEscape(pv.Uri.AbsolutePath);
				}
			Console.WriteLine (filelist);
			}

			System.Diagnostics.Process exigui = System.Diagnostics.Process.Start ("exigui", filelist); 
				exigui.WaitForExit ();

		}
		private static string CheapEscape (string input)
		{
			string escaped = input;
			escaped = escaped.Replace (" ", "\\ ");
			escaped = escaped.Replace ("(", "\\(");
			escaped = escaped.Replace (")", "\\)");
			return escaped;
		}

	}
}



