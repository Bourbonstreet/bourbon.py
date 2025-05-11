import requests
import pyttsx3
import pyaudio
import vosk
import json
import os
from PIL import Image
import io
import threading
import time

class DogImageAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.model_path = r"C:\Program Files\Python312\vosk-model-en-us-0.22"
        if not os.path.exists(self.model_path):
            raise ValueError(f"Vosk model not found at {self.model_path}")
        self.model = vosk.Model(self.model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                     channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=8000)

        self.current_image_data = None
        self.current_image_url = None
        self.current_breed = None
        self.commands = {
            "show": self.show_image,
            "save": self.save_image,
            "next": self.next_image,
            "name breed": self.name_breed,
            "resolution": self.get_resolution,
            "help": self.help_command
        }

        self.running = False

    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for voice commands"""
        print("Listening... (say 'help' for commands)")
        while self.running:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                command = result.get('text', '').lower()
                if command:
                    print(f"User: {command}")
                    self.process_command(command)

    def process_command(self, command):
        """Process the recognized command"""
        matched = False
        for cmd, action in self.commands.items():
            if cmd in command:
                try:
                    action()
                    matched = True
                    break
                except Exception as e:
                    print(f"Error executing command: {e}")
                    self.speak("Sorry, there was an error processing your command.")
                    matched = True
                    break

        if not matched:
            self.speak("Command not recognized. Please try again or say 'help' for available commands.")

    def fetch_dog_image(self):
        """Fetch a random dog image from the API"""
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            response.raise_for_status()
            data = response.json()

            self.current_image_url = data['message']
            self.current_breed = self.current_image_url.split('/')[-2]

            img_response = requests.get(self.current_image_url)
            img_response.raise_for_status()
            self.current_image_data = img_response.content

            return True
        except requests.RequestException as e:
            print(f"Error fetching dog image: {e}")
            self.speak("Sorry, I couldn't fetch a dog image. Please try again later.")
            return False

    def show_image(self):
        """Show the current dog image"""
        if not self.current_image_data:
            if not self.fetch_dog_image():
                return

        try:
            img = Image.open(io.BytesIO(self.current_image_data))
            img.show()
            self.speak(f"Here's a random dog image. Breed: {self.current_breed}")
        except Exception as e:
            print(f"Error displaying image: {e}")
            self.speak("Sorry, I couldn't display the image.")

    def save_image(self):
        """Save the current dog image to a file"""
        if not self.current_image_data:
            if not self.fetch_dog_image():
                return

        try:
            filename = f"dog_{self.current_breed}_{int(time.time())}.jpg"
            with open(filename, 'wb') as f:
                f.write(self.current_image_data)
            self.speak(f"Image saved as {filename}")
        except Exception as e:
            print(f"Error saving image: {e}")
            self.speak("Sorry, I couldn't save the image.")

    def next_image(self):
        """Fetch and show the next random dog image"""
        if self.fetch_dog_image():
            self.show_image()

    def name_breed(self):
        """Say the name of the current dog breed"""
        if not self.current_breed:
            if not self.fetch_dog_image():
                return

        self.speak(f"The breed is {self.current_breed.replace('-', ' ')}")

    def get_resolution(self):
        """Get and speak the resolution of the current image"""
        if not self.current_image_data:
            if not self.fetch_dog_image():
                return

        try:
            img = Image.open(io.BytesIO(self.current_image_data))
            width, height = img.size
            self.speak(f"The image resolution is {width} by {height} pixels")
        except Exception as e:
            print(f"Error getting resolution: {e}")
            self.speak("Sorry, I couldn't get the image resolution.")

    def help_command(self):
        """List available commands"""
        commands_list = ", ".join(self.commands.keys())
        self.speak(f"Available commands are: {commands_list}")

    def start(self):
        """Start the voice assistant"""
        self.running = True
        self.speak("Dog Image Assistant started. How can I help you?")

        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the voice assistant"""
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.speak("Dog Image Assistant stopped. Goodbye!")


if __name__ == "__main__":
    try:
        assistant = DogImageAssistant()
        assistant.start()
    except Exception as e:
        print(f"Error starting assistant: {e}")