
from tts.volcengine import generate_voice_file
from pathlib import Path
import sys

def tts(text: str):
    print(generate_voice_file(text))

if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    tts_dir = current_file.parent
    sys.path.append(str(tts_dir))

    def t1():
        tts("echo everbody")

    t1()