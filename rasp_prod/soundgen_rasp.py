import numpy as np
import pyaudio


def generate_audio(angle):
    '''Generate audio based on angle value'''
    # Generate the sine wave
    sample_rate = 44100 # fs
    # Changing the number of samples changes the frequency
    duration = 0.3
    array = np.arange(duration*sample_rate)
    zero = np.zeros(int(duration*sample_rate), dtype= float).astype(np.float32)

    
    if angle > 0 and angle != 100:
# Set the amplitude and frequency
        A = 0.08*np.sqrt(angle)
        f = 3.8*angle+ 230
        samples = A*(np.sin(2*np.pi*array*f/sample_rate)).astype(np.float32)
        # Save stereo samples
        stereo_samples = np.column_stack((zero, samples))

    elif angle < 0 and angle != 100: 
        A = 0.08*np.sqrt(-angle)
        f = 3.8*(-angle) + 230
        samples = A*(np.sin(2*np.pi*array*f/sample_rate)).astype(np.float32)
        # Save stereo samples
        stereo_samples = np.column_stack((samples, zero))
       
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=sample_rate, output=True)
    stream.write(stereo_samples.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()
