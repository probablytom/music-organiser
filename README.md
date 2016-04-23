#Music-organiser: does what it says on the tin

A script for organising a collection of music. 

Supports specification of source for music files, destination for the sorted collection, and a format the resulting filesystem should take. 

---

## Organisation

The format is the clever bit. Specify a structure for the collection to take with the --structure flag, followed by one of:

- artist
- album
- title
- track (the track number)
- genre

Music organiser will take all of the music files it finds of supported formats, and will name them with that tag, which it reads from the metadata in the file!

Oh, you want your files organised nearly into folders, not just named and all thrown into the same place? *Fine.* Specify tag/othertag, and the resulting structure will be the files put into the folders named by the first tag, and named by othertag.

You can specify as many folder as you'd like. 

Oh, you want to concatenate two tags together? *Fine.* Specify tag/othertag+thirdtag, and the files will be put into a *tag* directory, and named "othertagvalue - thirdtagvalue".filetype. 

This will work on filenames and folders. 

---

## Warnings and important information

The script doesn't currently handle missing tag information very well at all, so use with caution. 

It'll move files, rather than copying them, unless you're going between two different drives, like a hard drive and a USB drive. 

---

## Currently supported filetypes:

- .mp3
- .flac
- .aiff

Feel free to make a pull request and contribute more!
