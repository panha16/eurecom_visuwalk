import numpy as np
import pyaudio
import time


def generate_audio(gamma):
    '''Generate audio based on angle value'''
    # Generate the sine wave
    sample_rate = 44100 # fs
    # Changing the number of samples changes the frequency
    duration = 0.3
    array = np.arange(duration*sample_rate)
    zero = np.zeros(int(duration*sample_rate), dtype= float).astype(np.float32)
    angle = gamma.value

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=sample_rate, output=True)

    while(True):
        angle = gamma.value
        if angle != 100:    # out of bound value that indicates that no line was detected
            # Set the amplitude and frequency
            A = 0.08*np.sqrt(abs(angle))
            f = 3.8*abs(angle)+ 230
            samples = A*(np.sin(2*np.pi*array*f/sample_rate)).astype(np.float32)

            if abs(angle) < 3: # small angle : sound in both ears
                A = 0.03
                f = 230
                samples = A*(np.sin(2*np.pi*array*f/sample_rate)).astype(np.float32)
                # Save stereo samples
                stereo_samples = np.column_stack((samples, samples))
            elif angle < 0:
                stereo_samples = np.column_stack((zero, samples))
            elif angle > 0:
                stereo_samples = np.column_stack((samples, zero))

            stream.write(stereo_samples.tobytes())
        time.sleep(0.6)

    stream.stop_stream()
    stream.close()
    p.terminate()
