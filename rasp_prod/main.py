from multiprocessing import Process, Value

from soundgen_rasp import generate_audio
from improc_rasp import get_angle


if __name__ == "__main__":
    angle = Value('d', 100)
    Process(target=get_angle, args=(angle,)).start()
    Process(target=generate_audio, args=(angle,)).start()

