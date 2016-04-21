import fnmatch
import mutagen.easyid3
import shutil
import os

# TODO: Accept layout structure as parameter
# TODO: Accept path to sort as parameter
# TODO: Accept path for music to be sorted into as parameter




# TODO: Complete this!


class FileNotAcceptedTypeException(Exception):
    pass


# TODO: give this class necessary init code to get mutagen objects for any accepted filetype
# TODO: give this class methods for finding metadata tags from any arbitrary filetype (worth having subclasses for each type?)
class Music:
    def __init__(self, filepath):
        self.path = filepath
        self.audio = mutagen.easyid3.EasyID3(filepath)

    def get_artist(self):
        if self.audio is None: return None
        return self.audio['artist'][0].decode()

    def get_album(self):
        if self.audio is None: return None
        return self.audio['album'][0].decode()

    def get_title(self):
        if self.audio is None: return None
        return self.audio['title'][0].decode()

    def get_type(self):
        return self.path.split(".")[-1]


class MusicCollection:
    def __init__(self):
        self.collection = []
    def add_music(self, filename):
        self.collection.append(Music(filename))
    def pop_music(self):
        self.collection.pop()


music_collection = MusicCollection()
file_extensions_accepted = ['mp3']


def get_music_to_sort(path='./'):
    for root, dirnames, filenames in os.walk(path):
        print root, dirnames, filenames
        for filetype in file_extensions_accepted:
            for filename in fnmatch.filter(filenames, "*."+filetype):
                print os.path.join(root, filename)
                music_collection.add_music(os.path.join(root, filename))

def sort_music(path='./'):
    for track in music_collection.collection:
        new_filepath = path + track.get_artist() + "/" + track.get_album() + "/" + track.get_title() + "." + track.get_type()
        print new_filepath
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

