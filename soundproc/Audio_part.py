import numpy as np
from scipy.io.wavfile import write
import pyaudio
import random
import time


for i in range (10):
    angle = random.uniform(-70,70)


    if angle > 0 :
# Set the amplitude and frequency
        A_right = 0.08*np.sqrt(angle)
        f_right = 3.8*angle + 230
        A_left = 0
        f_left = 1

    else : 
        A_right = 0
        f_right = 1
        A_left = 0.08*np.sqrt(np.abs(angle))
        f_left = 3.8*(-angle) + 230
        

    # Generate the sine wave
    Freq_R = []
    Freq_L = []
    sample_rate = 44100 # fs
    # Changing the number of samples changes the frequency
    array = np.linspace(0,sample_rate,44100) #here we can change the last argument if we want shorter frames but it also changes the frequency
    samples_right = (np.sin(2*np.pi*array*f_right/sample_rate)).astype(np.float32)
    samples_right *= A_right
    samples_left = (np.sin(2*np.pi*array*f_left/sample_rate)).astype(np.float32)
    samples_left *= A_left

    # Save stereo samples
    stereo_samples = np.column_stack((samples_left, samples_right))

    # Save the sine wave to a WAV file
    write("sine_wave.wav", sample_rate, stereo_samples)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=sample_rate, output=True)
    stream.write(stereo_samples.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()
    i += 1

