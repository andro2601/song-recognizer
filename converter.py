import pydub
import numpy as np
import ffmpeg

def read(file, format, normalized=False):
    a = pydub.AudioSegment.from_file(file=file, format=format)
    output = np.array(a.get_array_of_samples())
    
    if a.channels == 2:
        output = output.reshape((-1, 2))
    
    if normalized:
        return a.frame_rate, np.float32(output) / 2**15
    else:
        return a.frame_rate, output

def write(file, input, sample_rate, normalized, format, bitrate):
    channels = 2 if (input.ndim == 2 and input.shape[1] == 2) else 1
    
    output = np.array()
    if normalized:
        output = np.int16(input*2**15)
    else:
        output = np.int16(input)
    
    song = pydub.AudioSegment(
        output.tobytes(), 
        frame_rate=sample_rate, 
        sample_width=2,
        channels=channels
        )
    
    song.export(file, format=format, bitrate=bitrate)
    