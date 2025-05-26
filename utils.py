import math
import librosa
import matplotlib.pyplot as plt
import numpy as np


### COSINE SIMILARITY OF TWO VECTORS WITH VARIABLE DIMENSIONS
def cosine_similarity(word_freq_unknown: dict, word_freq_reference: dict):
    if not word_freq_unknown and not word_freq_reference: return 0
    if not word_freq_unknown or not word_freq_reference: return 0
    
    x = 0
    y = 0
    z = 0
    
    for i in word_freq_unknown:
        a = word_freq_unknown[i]*(i/100)
        y += a*a
        if i in word_freq_reference:
            b = word_freq_reference[i]*(i/100)
            x += a*b
            z += b*b
    
    if y == 0 or z == 0: return 0
    
    return x / (math.sqrt(y) * math.sqrt(z))


### CHROMAPRINT MATCHING ALGORITHM
def match_fingerprints(melody_unknown: list[str], melody_reference: list[str]):
    i = 0
    j = 0
    matches = 0
    numChunks = len(melody_unknown)
    
    while i < numChunks:
        back = max(0, max(i-5, min(j, i)))
        forward = min(numChunks, i+5)
        
        if melody_unknown[i] in melody_reference[back:forward]:
            matches += 1
            j = i

        i += 1
        
    return matches/numChunks


### SORTS NESTED LIST ARGUMENTS, USED IN CREATING FINGERPRINT
def argsort(l: list, reversed: bool):
    li=[]
 
    for i in range(len(l)):
        li.append([l[i],i])
        
    li = sorted(li, reverse=reversed)
    sort_index = []
    
    for x in li:
        sort_index.append(x[1])
    
    return sort_index


### FORMATS PATH AND FILE NAME TO THE STANDARD REQUIREMENTS
def format_path(artist: str, song: str, version: str) -> str:
    return '/'.join(['pjesme', artist, song, '_'.join([artist, song, version]).replace(' ', '+')])+ '.mp3'


### PLOTS CHROMAGRAM
def plot(chroma):
    librosa.display.specshow(np.transpose(chroma), x_axis='time', y_axis='chroma')
    plt.colorbar()
    plt.show()


### CALCULATES THE TOTAL OUTPUT OF MATCHING ALGORITHM
def cumulative_probabilities(lyrics_matches: list, chroma_matches: list) -> list:
    lfactor = (1 - (lyrics_matches[1][0] / lyrics_matches[0][0])) if lyrics_matches[0][0] > 0 else 0
    cfactor = (1 - (chroma_matches[1][0] / chroma_matches[0][0])) if chroma_matches[0][0] > 0 else 0
    
    sumfactor = lfactor+cfactor
    lfactor = (lfactor/(sumfactor)) if sumfactor > 0 else 0
    cfactor = (cfactor/(sumfactor)) if sumfactor > 0 else 0
    
    lsorted = sorted(lyrics_matches, key=lambda x: x[1])
    csorted = sorted(chroma_matches, key=lambda x: x[1])
    
    probs = []
    for i in range(len(lsorted)):
        l = lfactor * lsorted[i][0]
        c = cfactor * csorted[i][0]
        
        probs.append([l+c, lsorted[i][1]])
    
    return probs