import pyttsx3
import speech_recognition as sr
import threading

class SpeechRecognizer(threading.Thread):

    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


    def get_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for ambient noise levels
            self.recognized_text += "Listening...\n"

            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
            except Exception as e:
                print("Exception:", str(e))

        return said.lower()

    def __init__(self, TOTAL_PATTERNS, COUNTRY_PATTERNS, country_list, data):
        super(SpeechRecognizer, self).__init__()
        self.setDaemon(True)
        self.recognized_text = "Initializing\n"
        self.TOTAL_PATTERNS = TOTAL_PATTERNS
        self.COUNTRY_PATTERNS = COUNTRY_PATTERNS
        self.country_list = country_list
        self.data = data

    def run(self):
        UPDATE_COMMAND = "update"
        END_PHRASE = "stop"
        while True:
            # print("Listening...\n")
            text = self.get_audio()
            self.recognized_text += text + "\n"
            result = None

            for pattern, func in self.COUNTRY_PATTERNS.items():
                if pattern.match(text):
                    words = set(text.split(" "))
                    for country in self.country_list:
                        if country in words:
                            result = func(country)
                            break

            for pattern, func in self.TOTAL_PATTERNS.items():
                if pattern.match(text):
                    result = func()
                    break

            if text == UPDATE_COMMAND:
                result = "Data is being updated. This may take a moment!"
                self.recognized_text += self.data.update_data()

            if result:
                self.speak(result)

            if text.find(END_PHRASE) != -1:  # stop loop
                self.recognized_text += "Exit\n"
                break
