import mysql.connector
import os
import json
import shutil
import utils

mydb = mysql.connector.connect(
    host="localhost",
    user="andrija",
    password="*****", # password
    database="music"
)

cursor = mydb.cursor()

### MAKE WORD FREQUENCY DICTIONARY FROM LIST OF WORDS GATHERED FROM LYRICS
def lyric_processing(lyrics: list[str]):
    findWord = "SELECT id FROM commonwords WHERE word LIKE %s"
    word_count = {}
    
    for word in lyrics:
        cursor.execute(findWord, (word,))
        i = cursor.fetchone()
        if not i: continue
        
        i = i[0]
        if (i in word_count):
            word_count[i] += 1
        else:
            word_count.update({i: 1})  
    
    return word_count


### SAVE IDENTIFIED SONG
def save_new_song_version(songID: int, version: str, lyrics: dict, melody: list[str]):
    insertSongVersion = "INSERT INTO songVersions (songID, version, lyrics, fingerprint) VALUES(%s, %s, %s, %s)"
    
    lyrics = json.dumps(lyrics)
    melody = ';'.join(chunk for chunk in melody)
    
    while version in get_song_versions(songID):
        version = input('The provided version already exists. Please provide another song version name: ')
    
    cursor.execute(insertSongVersion, (songID, version, lyrics, melody))

    mydb.commit()
    
    artist, song = get_song(songID)
    path = utils.format_path(artist, song, version)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(shutil.copy('resursi/input.mp3', path))
    

### CREATE NEW ROW IN SONGS TABLE
def save_new_song(artist: str, song: str) -> int:
    cursor.execute("INSERT INTO songs (artist, song) VALUES(%s, %s)", (artist, song))
    mydb.commit()
    
    cursor.execute("SELECT id FROM songs WHERE artist LIKE %s AND song LIKE %s", (artist, song))
    return int(cursor.fetchone()[0])
    
    
### FETCH DETAILS ABOUT PRETICULAR SONG VERSION
def fetch_all():
    cursor.execute("SELECT * FROM songversions")

    versions = cursor.fetchall()
    
    for v in versions:
        songID = v[0]
        version = v[1]
        lyrics = json.loads(v[2], object_hook=lambda d: {int(k): v for k, v in d.items()})
        melody = v[3].decode('utf-8').split(';')

        yield songID, version, lyrics, melody


### INSERT SONGS FROM FOLDERS
def add_songs(songs_folder: str):
    songs_folder = 'pjesme'
    
    insertSong = "INSERT INTO songs (artist, song) VALUES (%s, %s)"

    for artist in os.listdir(songs_folder):
        artist_folder = '\\'.join((songs_folder, artist))
        if os.path.isdir(artist_folder):
            for song in os.listdir(artist_folder):
                song_folder = '\\'.join((artist_folder, song))
                if os.path.isdir(song_folder):
                    cursor.execute(insertSong, (artist, song))


### GET SONG ID FROM SONG NAME AND ARTIST NAME
def get_songID(song: str, artist: str) -> int:
    cursor.execute("SELECT id FROM songs WHERE artist LIKE %s AND song LIKE %s", (artist, song))
    
    result = cursor.fetchone()
    if not result:
        return -1
    
    return result[0]


### GET SONG NAME AND ARTIST NAME FROM SONG ID
def get_song(songID: int) -> tuple[str]:
    cursor.execute("SELECT artist, song FROM songs WHERE id = %s", (songID,))
    artist, song = cursor.fetchone()
    
    return artist, song


### GET SONG VERSIONS FROM SONG ID
def get_song_versions(songID: int) -> tuple[str]:
    cursor.execute("SELECT version FROM songversions WHERE songID = %s", (songID,))
    
    return tuple(item[0] for item in cursor.fetchall())