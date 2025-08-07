from time import strftime

import speech_recognition as sr
import win32com.client
import webbrowser
import openai
import datetime
# Initialize the SAPI voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def takeCommand():
    """Listens for microphone input and returns the recognized text as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # Adjust for ambient noise to improve accuracy
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Using Google's recognizer which doesn't require an API key for basic use
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"


if __name__ == '__main__':
    # Greet the user once at the start
    speaker.Speak("Hello, I am your voice assistant")

    while True:
        # Get the command from the user
        command = takeCommand().lower()  # Convert to lowercase for easier matching

        # If nothing was recognized, continue the loop
        if command == "none":
            continue

        if 'the time' in command:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.speak(f"The time is {time}")

        if command.lower().startswith('open'):
            site=command[5:].strip()
            speaker.speak(f'Opening {site}')
            webbrowser.open(f'https://www.{site}.com/')

        # Speak the recognized command back to the user
        speaker.Speak(f"You said: {command}")

        # Add a condition to exit the loop
        if "exit" in command or "stop" in command:
            speaker.Speak("Goodbye!")
            break