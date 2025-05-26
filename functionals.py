import numpy as np
from transcription import transcribe
import database
import utils
import librosa

### CREATES CHUNKS OF CHROMAPRINT
def fingerprinter(indexes: list, chunk_size: int, xover: int):
    i = 0
    while i < len(indexes):
        if i+chunk_size >= len(indexes): break
        
        res = ''.join([str(hex(ele))[2:] for ele in indexes[i:i+chunk_size]])
        yield res
        
        i = i + chunk_size - xover


### EXTRACTS FEATURES FROM INPUT FILE
def extract_features(file: str, fingerprint: str, language: str, begin_vocals=0):
    y, sr = librosa.load(file)
    y, i = librosa.effects.trim(y)
    chroma = np.transpose(librosa.feature.chroma_cens(y=y, sr=sr))
    utils.plot(chroma)

    maxes = [np.argsort(subarr)[-1] for subarr in chroma]
    chunk_size = 5
    xover = 1
    
    chunks = [chunk for chunk in fingerprinter(maxes, chunk_size, xover)]

    with open(fingerprint, 'w+', newline='') as out:
        out.write(chunks[0])
        for chunk in chunks[1:]:
            out.write(';' + chunk)
    
    lyrics = transcribe(file, language, begin_vocals)
    
    return lyrics, chunks


### STORES NEW SONG WITH SPECIFIED PARAMETERS
def save_song(song: str, artist: str, version: str, language: str, begin_vocals=0):
    file = 'resursi/input.mp3'
    fingerprint = 'resursi/fingerprint.csv'

    lyrics, melody = extract_features(file, fingerprint, language, begin_vocals)
    lyrics = database.lyric_processing(lyrics)
    
    songID = database.get_songID(song, artist)
    
    if songID == -1:
        songID = database.save_new_song(artist, song)
    
    database.save_new_song_version(songID, version, lyrics, melody)


### ATTEMPTS TO IDENTIFY SONG FROM UNKNOWN AUDIO INPUT GIVEN LANGUAGE OF LYRICS
def identify_song(language: str, begin_vocals=0):
    file = 'resursi/input.mp3'
    fingerprint = 'resursi/fingerprint.csv'

    lyrics, melody_unknown = extract_features(file, fingerprint, language, begin_vocals)
    
    word_freq_unknown = database.lyric_processing(lyrics)
    
    matches = {}
    
    versions = database.fetch_all()
    
    for songID, version, freq_reference, melody_reference in versions:
        #print(freq_reference)
        lyrics_match = utils.cosine_similarity(word_freq_unknown, freq_reference)
        melody_match = utils.match_fingerprints(melody_unknown, melody_reference)
        
        if songID in matches:
            matches[songID].update({version: {'lyrics': lyrics_match, 'melody': melody_match}})
        else:
            matches.update({songID: {version: {'lyrics': lyrics_match, 'melody': melody_match}}})
    
    max_lyrics_matches = []
    max_melody_matches = []
    
    for songID in matches:
        max_lyrics_match = 0
        max_melody_match = 0
        
        i = 0
        for version in matches[songID]:
            lyrics_match = matches[songID][version]['lyrics']
            melody_match = matches[songID][version]['melody']
            if lyrics_match > max_lyrics_match: max_lyrics_match = lyrics_match
            if melody_match > max_melody_match: max_melody_match = melody_match
            i += 1
        
        max_lyrics_matches.append([max_lyrics_match, songID])
        max_melody_matches.append([max_melody_match, songID])
    
    max_lyrics_matches = sorted(max_lyrics_matches, key=lambda x: x[0], reverse=True)
    max_melody_matches = sorted(max_melody_matches, key=lambda x: x[0], reverse=True)
    
    total_matches = utils.cumulative_probabilities(max_lyrics_matches, max_melody_matches)
    
    total_matches = sorted(total_matches, key=lambda x: x[0], reverse=True)
    
    print(max_lyrics_matches[:3])
    print(max_melody_matches[:3])

    i = 1
    for match in total_matches[:3]:
        percentage = match[0]
        songID = match[1]
        artist, song = database.get_song(songID)
        
        print(str(i) + '. match = [' + ' - '.join([artist, song]) + '] with certainty = ' + str(round(percentage, 4)*100) + '%')
        
        i += 1
        
    choice = input('Type [' + '|'.join([str(choice) for choice in range(1, i)]) + '] to save audio as that song or [n] to save as new song: ')
    
    while choice != 'n' and int(choice) not in range(1, i):    
        choice = int(input())
    
    if choice == 'n':
        artist = input('Provide artist name: ')
        song = input('Provide song name: ')
        songID = database.get_songID(song, artist)
        if songID == -1:
            songID = database.save_new_song(artist, song)
    else:
        songID = total_matches[int(choice)-1][1]
        
    version = input('Please provide song version name: ')
    
    while version in database.get_song_versions(songID):
        version = input('The provided version already exists. Please provide another song version name: ')
        
    database.save_new_song_version(songID, version, word_freq_unknown, melody_unknown)