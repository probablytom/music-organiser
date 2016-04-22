import fnmatch
import argparse
import shutil
import os
import mutagen.flac
import mutagen.easyid3

# TODO: Accept layout structure as parameter
# TODO: Accept path to sort as parameter
# TODO: Accept path for music to be sorted into as parameter
# TODO: Set up argparse


class FileNotAcceptedTypeException(Exception):
    pass


class NoAudioObjectException(Exception):
    pass


class AbstractOggVorbCommentParser:
    def __init__(self, filepath):
        self.path = filepath
        self.audio = None


    def get_artist(self):
        if self.audio is None: raise NoAudioObjectException
        else: return self.audio.tags["artist"][0].decode()


    def get_genre(self):
        if self.audio is None: return None
        return self.audio.tags["genre"][0].decode()


    def get_track(self):
        if self.audio is None: return None
        return self.audio.tags["tracknumber"][0].decode()


    def get_album(self):
        if self.audio is None: return None
        return self.audio.tags["album"][0].decode()


    def get_title(self):
        if self.audio is None: return None
        return self.audio.tags["title"][0].decode()


    def get_type(self):
        return self.path.split(".")[-1]


# TODO: give this class necessary init code to get mutagen objects for any accepted filetype
# TODO: give this class methods for finding metadata tags from any arbitrary filetype (worth having subclasses for each type?)
class MP3:
    def __init__(self, filepath):
        self.path = filepath
        self.audio = mutagen.easyid3.EasyID3(filepath)  # What if we fail? Should raise an exception.

    def get_artist(self):
        return self.audio['artist'][0].decode()

    def get_album(self):
        return self.audio['album'][0].decode()

    def get_title(self):
        return self.audio['title'][0].decode()

    def get_type(self):
        return self.path.split(".")[-1]


class Flac(AbstractOggVorbCommentParser):
    def __init__(self, filepath):
        super(Flac, self).__init__(filepath)  # What if we fail? Should raise an exception.
        self.audio = mutagen.flac.FLAC(filepath)


class MusicCollection:
    def __init__(self):
        self.collection = []
    def add_music(self, filename):
        ext = filename.split('.')[-1]
        self.collection.append(file_extensions_accepted[ext](filename))
    def pop_music(self):
        self.collection.pop()


music_collection = MusicCollection()
file_extensions_accepted = {'mp3': MP3,
                            'flac': Flac}



def get_music_to_sort(path='./'):
    for root, dirnames, filenames in os.walk(path):
        print root, dirnames, filenames
        for filetype in file_extensions_accepted.keys():
            for filename in fnmatch.filter(filenames, "*."+filetype):
                print os.path.join(root, filename)
                music_collection.add_music(os.path.join(root, filename))

def sort_music(path='./'):
    for track in music_collection.collection:
        print track.get_artist(), track.get_album(), track.get_title(), track.get_type()
        new_filepath = path + track.get_artist() + "/" + track.get_album() + "/" + track.get_title() + "." + track.get_type()
        if not os.path.exists(os.path.dirname(new_filepath)):
            os.makedirs(os.path.dirname(new_filepath))
            print "Made path!"
        try:
            shutil.move(track.path, new_filepath)
            track.path = new_filepath
        except:
            print "Couldn't move track at " + track.path + "!"


if __name__ == "__main__":
    get_music_to_sort()
    sort_music()

