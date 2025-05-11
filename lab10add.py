import requests
import pyttsx3
import pyaudio
import vosk
import json
import webbrowser
from threading import Thread
import time


class DictionaryVoiceAssistant:
    def __init__(self):

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # English voice


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

        self.current_word = None
        self.current_data = None

        self.commands = {
            "find": self.find_word,
            "meaning": self.get_meaning,
            "example": self.get_example,
            "link": self.open_link,
            "save": self.save_data,
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
                    if cmd == "find":
                        word = command.replace("find", "").strip()
                        if word:
                            action(word)
                        else:
                            self.speak("Please specify a word to find. Say 'find' followed by the word.")
                    else:
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

    def fetch_word_data(self, word):
        """Fetch word data from the dictionary API"""
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            response.raise_for_status()
            self.current_data = response.json()
            self.current_word = word
            return True
        except requests.exceptions.HTTPError:
            self.speak(f"Sorry, I couldn't find information about the word '{word}'.")
            return False
        except requests.RequestException as e:
            print(f"Error fetching word data: {e}")
            self.speak("Sorry, I couldn't connect to the dictionary service. Please try again later.")
            return False

    def find_word(self, word):
        """Find information about a word"""
        if self.fetch_word_data(word):
            self.speak(f"Found information about {word}. You can now ask for meanings or examples.")

    def get_meaning(self):
        """Get the meaning of the current word"""
        if not self.current_data:
            self.speak("No word has been searched yet. Please say 'find' followed by a word.")
            return

        try:
            meanings = []
            for entry in self.current_data:
                for meaning in entry.get('meanings', []):
                    for definition in meaning.get('definitions', []):
                        meanings.append(definition.get('definition', ''))

            if meanings:
                self.speak(f"The meanings of {self.current_word} are: {' '.join(meanings[:3])}")  # Limit to 3 meanings
            else:
                self.speak(f"Sorry, I couldn't find any meanings for {self.current_word}.")
        except Exception as e:
            print(f"Error getting meaning: {e}")
            self.speak("Sorry, I couldn't retrieve the meanings.")

    def get_example(self):
        """Get an example usage of the current word"""
        if not self.current_data:
            self.speak("No word has been searched yet. Please say 'find' followed by a word.")
            return

        try:
            examples = []
            for entry in self.current_data:
                for meaning in entry.get('meanings', []):
                    for definition in meaning.get('definitions', []):
                        if 'example' in definition:
                            examples.append(definition['example'])

            if examples:
                self.speak(f"An example for {self.current_word} is: {examples[0]}")  # Use first example
            else:
                self.speak(f"Sorry, I couldn't find any examples for {self.current_word}.")
        except Exception as e:
            print(f"Error getting example: {e}")
            self.speak("Sorry, I couldn't retrieve an example.")

    def open_link(self):
        """Open the dictionary API link in browser"""
        if not self.current_word:
            self.speak("No word has been searched yet. Please say 'find' followed by a word.")
            return

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.current_word}"
        webbrowser.open(url)
        self.speak(f"Opened the dictionary page for {self.current_word} in your browser.")

    def save_data(self):
        """Save the current word data to a file"""
        if not self.current_data:
            self.speak("No word has been searched yet. Please say 'find' followed by a word.")
            return

        try:
            filename = f"dictionary_{self.current_word}_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.current_data, f, indent=2)
            self.speak(f"Saved information about {self.current_word} to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
            self.speak("Sorry, I couldn't save the dictionary data.")

    def help_command(self):
        """List available commands"""
        commands_list = ", ".join(self.commands.keys())
        self.speak(f"Available commands are: {commands_list}. For example, say 'find computer' to look up a word.")

    def start(self):
        """Start the voice assistant"""
        self.running = True
        self.speak("English Dictionary Voice Assistant started. How can I help you?")

        listen_thread = Thread(target=self.listen)
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
        self.speak("Dictionary assistant stopped. Goodbye!")


if __name__ == "__main__":
    import os

    try:
        assistant = DictionaryVoiceAssistant()
        assistant.start()
    except Exception as e:
        print(f"Error starting assistant: {e}")