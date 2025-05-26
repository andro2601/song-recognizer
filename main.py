import sys
from functionals import save_song
from functionals import identify_song

### STORES NEW SONG WITH SPECIFIED ARGUMENTS
def store(args: list[str]):
    print(args)
    if len(args) != 8 and len(args) != 10:
        raise Exception('Must artist name, song name, version name and language!')

    artist = ''
    song = ''
    version = ''
    language = ''
    begin_vocals = 0

    for i in range(len(args)):
        tag = args[i].lower()
        if tag == '-a' or tag == '--artist':
            artist = args[i+1]
        elif tag == '-s' or tag == '--song':
            song = args[i+1]
        elif tag == '-v' or tag == '--version':
            version = args[i+1]
        elif tag == '-l' or tag == '--language':
            language = args[i+1]
        elif tag == '-b' or tag == '--begin-vocals':
            begin_vocals = int(args[i+1])

    save_song(song, artist, version, language, begin_vocals)


### ATTEMPTS TO IDENTIFY SONG
def classify(args: list[str]):
    if len(args) != 2 and len(args) != 4:
        raise Exception('Must specify language!')

    language = ''
    begin_vocals = 0

    for i in range(len(args)):
        tag = args[i].lower()
        if tag == '-l':
            language = args[i+1]
        elif tag == '-b':
            begin_vocals = int(args[i+1])

    identify_song(language, begin_vocals)
    

args = sys.argv
operation = args[1].lower()

if operation == 'classify':
    classify(args[2:])
    
elif operation == 'store':
    store(args[2:])

else:
    raise Exception('Unsupported operation!')