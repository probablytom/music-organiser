import fnmatch
import argparse
import shutil
import os
import mutagen
import mutagen.flac
import mutagen.easyid3

# TODO: Accept layout structure as parameter
# TODO: Accept path to sort as parameter
# TODO: Accept path for music to be sorted into as parameter


# NOTE: Audio classes must have get_artist, get_track, get_title, get_album and get_genre! No exceptions!


class PathGenerator:

    def __init__(self, format):
        self.format = format
        self.tags=format.split('/')

    def generate_path(self, audio):
        generated_path = ""
        for tag in self.tags[:-1]:
            try:
                generated_path += getattr(audio,"get_"+tag)() + "/"
            except AttributeError, NoTagFoundException:
                raise NoTagFoundException
        generated_path += getattr(audio, "get_" + self.tags[-1])() + "." + audio.get_type()
        return generated_path


class FileNotAcceptedTypeException(Exception):
    pass


class NoAudioObjectException(Exception):
    pass


# To be used if we can't find a necessary tag? Or ask the user?
class NoTagFoundException(Exception):
    pass


class AbstractOggVorbCommentParser:
    def __init__(self, filepath):
        self.path = filepath
        self.audio = None

    def get_artist(self):
        if self.audio is None:
            raise NoAudioObjectException
        else:
            return self.audio.tags["artist"][0].decode()

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

# What should happen if a key isn't filled in?
class AbstractID3Parser:
    def __init__(self, filepath):
        self.path = filepath
        self.audio = mutagen.File(filepath)  # What if we fail? Should raise an exception.

    def get_artist(self):
        print self.audio.tags
        return self.audio['TPE2'][0].decode()

    def get_album(self):
        return self.audio['TALB'][0].decode()

    def get_title(self):
        return self.audio['TIT2'][0].decode()

    # Genre?

    # Track?

    def get_type(self):
        return self.path.split(".")[-1]


class MP3(AbstractID3Parser):
    def __init__(self, filename):
        AbstractID3Parser.__init__(self, filename)


class AIFF(AbstractID3Parser):
    def __init__(self, filename):
        AbstractID3Parser.__init__(self, filename)


class Flac(AbstractOggVorbCommentParser):
    def __init__(self, filepath):
        AbstractOggVorbCommentParser.__init__(self, filepath)  # What if we fail? Should raise an exception.
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
                            'flac': Flac,
                            'aiff': AIFF}



def get_music_to_sort(path='./'):
    for root, dirnames, filenames in os.walk(path):
        for filetype in file_extensions_accepted.keys():
            for filename in fnmatch.filter(filenames, "*."+filetype):
                music_collection.add_music(os.path.join(root, filename))

def sort_music(format="artist/album/title", path='./'):
    path_generator = PathGenerator(format)
    if path[-1] is not "/": path += "/"
    for track in music_collection.collection:
        new_filepath = path + path_generator.generate_path(track)
        if not os.path.exists(os.path.dirname(new_filepath)):
            os.makedirs(os.path.dirname(new_filepath))
        try:
            shutil.move(track.path, new_filepath)
            track.path = new_filepath
        except:
            print "Couldn't move track at " + track.path + "!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Organizes a music collection using tag information.
    Directory structure defaults to artist/album/track, but can be extended via parameters.''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--structure', type=str, dest="format",
                    help="The filesystem structure desired.\n"+ \
                         "The structure should be a string, with slashes separating the folders. The last tag will be the filename.\n"+ \
                         "For the default, then, the format is:\n\tartist/album/track\n"
                         "Supported tags:"+ \
                         "\tartist\n"+ \
                         "\talbum\n"+ \
                         "\tgenre\n"+ \
                         "\ttrack\n"+ \
                         "\ttitle\n")
    args = parser.parse_args()
    get_music_to_sort()
    sort_music()

