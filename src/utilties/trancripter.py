import wave
import json
from vosk import Model, KaldiRecognizer
import os

class Transcriber:
    def __init__(self,audio_file):
        self.model_path = r"C:\Users\Naman Agrawal\OneDrive\Documents\Final_year project\Clipscript\vosk-model-small-hi-0.22"
        self.model = None
        self.audio_file = audio_file
        self.transcribe_file(self.audio_file)

    def load_model(self):
        if self.model is None:
            print("Loading model...")
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model not found at {self.model_path}")
            self.model = Model(self.model_path)
            print("Model loaded successfully.")
        else:
            print("Model already loaded.")

    def transcribe_file(self, file_path):
        print(file_path)
        self.load_model()  

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at {file_path}")

        wf = wave.open(file_path, "rb")

        if wf.getnchannels() != 1 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be mono and 16kHz")

        recognizer = KaldiRecognizer(self.model, wf.getframerate())

        print("Transcribing audio...")
        transcription = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                transcription.append(text)
                print(text)

        final_result = recognizer.FinalResult()
        final_text = json.loads(final_result)["text"]
        transcription.append(final_text)
        print(f"Final Transcript: {final_text}")

        return " ".join(transcription)

    def save_transcription(self, transcription, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print(f"Transcription saved to {output_file}")

