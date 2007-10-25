/*
 * RawPlusJpegExiflow.cs
 *
 * Author(s)
 * 	Ulf Rompe <f-spot.org@rompe.org>
 *
 * Heavily based on the original RawPlusJpeg extension written by
 * 	Stephane Delcroix  <stephane@delcroix.org>
 *
 * This is free software. See COPYING for details
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;

using Gtk;

using FSpot;
using FSpot.Extensions;

namespace RawPlusJpegExiflowExtension
{
	public class RawPlusJpegExiflow : ICommand
	{
		public void Run (object o, EventArgs e)
		{
			Console.WriteLine ("EXECUTING RAW PLUS JPEG EXTENSION");

			if (ResponseType.Ok != HigMessageDialog.RunHigConfirmation (
				MainWindow.Toplevel.Window,
				DialogFlags.DestroyWithParent,
				MessageType.Warning,
				"Merge Raw+Jpegs, exiflow style",
				"This operation will merge Raw and Jpegs versions, including exiflow ( http://exiflow.sf.net/ ) revisions, of the same image as one unique image. The Raw image will be the Original version, the jpeg will be named 'Jpeg' and all subsequent versions will keep their original names (if possible).\n\nNote: only enabled for some formats right now.",
				"Do it now"))
				return;

			Photo [] photos = Core.Database.Photos.Query ((Tag [])null, null, null, null);
			Array.Sort (photos, new CompareName ());

			Photo previousphoto = null;

			IList<MergeRequest> merge_requests = new List<MergeRequest> ();
			ArrayList currentphotos = new ArrayList ();

			for (int i = 0; i < photos.Length; i++) {
				Photo p = photos [i];

				if (p != null && previousphoto != null && !ExiflowMatch(p, previousphoto)) {
					if (currentphotos.Count > 1) {
						ExiflowMerge(currentphotos);
					}
					currentphotos.Clear();
				}
				currentphotos.Add(p);
				previousphoto = p;
			}
			if (currentphotos.Count > 1) {
				ExiflowMerge(currentphotos);
			}
			
			MainWindow.Toplevel.UpdateQuery ();
		}

		private static bool ExiflowMatch (Photo p1, Photo p2)
		{
			String exiflowpat = "^\\d{8}-.{3}\\d{4}-.{5}\\.[^.]*$";
			return System.Text.RegularExpressions.Regex.IsMatch (p1.Name, exiflowpat) &&
				System.Text.RegularExpressions.Regex.IsMatch (p2.Name, exiflowpat) &&
				p1.Name.Substring (0, 19) == p2.Name.Substring (0, 19);
		}


		private static void ExiflowMerge (ArrayList photos)
		{
			photos.Sort(new CompareNameWithRaw ());
			Console.WriteLine ("Maybe merging these photos:");
			foreach (Photo photo in photos) {
				Console.WriteLine (photo.Name);
			}
		}

		/* IComparer to sort photos by name. */
		class CompareName : System.Collections.IComparer
		{
			public int Compare (object obj1, object obj2)
			{
				Photo p1 = (Photo)obj1;
				Photo p2 = (Photo)obj2;
				return String.Compare (p1.Name, p2.Name);
			}
		}

		/* IComparer to sort photos by type and then by name.
		 * Raw images are always ordered before other formats. */
		class CompareNameWithRaw : System.Collections.IComparer
		{
			public int Compare (object obj1, object obj2)
			{
				Photo p1 = (Photo)obj1;
				Photo p2 = (Photo)obj2;
				if (ImageFile.IsRaw(p2.Name)) {
					return 1;
				}
				return String.Compare (p1.Name, p2.Name);
			}
		}

		class MergeRequest 
		{
			Photo raw;
			Photo jpeg;

			public MergeRequest (Photo raw, Photo jpeg)
			{
				this.raw = raw;
				this.jpeg = jpeg;
			}

			public void Merge ()
			{
				Console.WriteLine ("Merging {0} and {1}", raw.VersionUri (Photo.OriginalVersionId), jpeg.VersionUri (Photo.OriginalVersionId));
				foreach (uint version_id in jpeg.VersionIds) {
					string name = jpeg.GetVersion (version_id).Name;
					try {
						raw.DefaultVersionId = raw.CreateReparentedVersion (jpeg.GetVersion (version_id) as PhotoVersion);
						if (version_id == Photo.OriginalVersionId)
							raw.RenameVersion (raw.DefaultVersionId, "Jpeg");
						else
							raw.RenameVersion (raw.DefaultVersionId, name);
					} catch (Exception e) {
						Console.WriteLine (e);
					}
				}
				uint [] version_ids = jpeg.VersionIds;
				Array.Reverse (version_ids);
				foreach (uint version_id in version_ids) {
					try {
						jpeg.DeleteVersion (version_id, true, true);
					} catch (Exception e) {
						Console.WriteLine (e);
					}
				}	
				Core.Database.Photos.Commit (raw);
				Core.Database.Photos.Remove (jpeg);
			}
		}
	}
}
