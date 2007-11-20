/*
 * DevelopInUFRawExiflow.cs
 *
 * Author(s)
 * 	Sebastian Berthold <exiflow@sleif.de>
 *
 * Heavily based on the original DevelopInUFRaw extension written by
 * 	Stephane Delcroix  <stephane@delcroix.org>
 *
 * This is free software. See COPYING for details
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;

using FSpot;
using FSpot.Extensions;
using Mono.Unix;

namespace DevelopInUFRawExiflowExtension
{
	public class DevelopInUFRawExiflow: ICommand
	{
		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING DEVELOP IN UFRawExiflow EXTENSION");
			
			foreach (Photo p in MainWindow.Toplevel.SelectedPhotos ()) {
				PhotoVersion raw = p.GetVersion (Photo.OriginalVersionId) as PhotoVersion;
				if (!ImageFile.IsRaw (raw.Uri.AbsolutePath)) {
					Console.WriteLine ("The Original version of this image is not a (supported) RAW file");
					continue;
				}

				string name = GetVersionName (p);
				System.Uri developed = GetUriForVersionName (p, name);
				string args = String.Format("--exif --overwrite --compression=95 --out-type=jpeg --output={0} {1}", 
					CheapEscape (developed.LocalPath),
					CheapEscape (raw.Uri.ToString()));
				Console.WriteLine ("ufraw "+args);

				System.Diagnostics.Process ufraw = System.Diagnostics.Process.Start ("ufraw", args); 
				ufraw.WaitForExit ();
				if (!(new Gnome.Vfs.Uri (developed.ToString ())).Exists) {
					Console.WriteLine ("UFraw didn't ended well. Check that you have UFRaw 0.13 (or CVS newer than 2007-09-06). Or did you simply clicked on Cancel ?");
					continue;
				}

				p.DefaultVersionId = p.AddVersion (developed, name, true);
				Core.Database.Photos.Commit (p);
			}	
		}

		private static string GetVersionName (Photo p)
		{
			return GetVersionName (p, 0);
		}

		private static string GetVersionName (Photo p, int i)
		{
			Regex exiflowpat = new Regex(@"^(\d{8}-.{3}\d{4}-.{2})(\d)(.{2}\.[^.]*$)");
			Match exiflowpatmatch = exiflowpat.Match(p.Name);
			string name = String.Format("{0}{1}00.jpg", exiflowpatmatch.Groups[1], i);
			if (p.VersionNameExists (name))
				return GetVersionName (p, i + 1);
			return name;
		}

		private System.Uri GetUriForVersionName (Photo p, string version_name)
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
