import speech_recognition as sr
import os
import webbrowser
import google.generativeai as genai
import datetime
import pyttsx3  # ---MODIFIED for Windows---

from config import apikey

genai.configure(api_key=apikey)
model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=[])
engine = pyttsx3.init()

def say(text):
    """
    This function uses the pyttsx3 text-to-speech engine to speak the given text.
    """
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


# This function is for more general AI prompts and saves the output to a file
def ai(prompt):
    """
    This function takes a prompt and uses the Gemini API to generate a response.
    The response is then saved to a text file.
    """
    print("Generating AI response...")
    # Add the spoken prompt to the output
    say(f"Generating an AI response for your prompt: {prompt}")
    text = f"Gemini response for Prompt: {prompt} \n *************************\n\n"

    try:
        # Call the Gemini API
        response = model.generate_content(prompt)
        text += response.text

        if not os.path.exists("Gemini_Responses"):
            os.mkdir("Gemini_Responses")

        # Sanitize the filename to remove invalid characters
        sanitized_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '.', '_')).rstrip()
        with open(f"Gemini_Responses/{sanitized_prompt}.txt", "w", encoding='utf-8') as f:
            f.write(text)

        say("Your response has been generated and saved to a file.")

    except Exception as e:
        print(f"An error occurred: {e}")
        say("Sorry, I couldn't process that request.")


def takeCommand():
    """
    This function listens for a command from the user through the microphone
    and returns the command as a string.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.energy_threshold = 400  # Adjust this based on your microphone's sensitivity
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "could not understand audio"
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "could not request results"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "some error occurred"


if __name__ == '__main__':
    say(" Virtual AI at your service")
    while True:
        query = takeCommand()

        # Error handling for failed command recognition
        if "error occurred" in query or "could not understand" in query or "could not request" in query:
            continue
        if query.lower().startswith('open'):
            site = query[5:].strip()
            say(f"Opening {site}...")
            webbrowser.open(f'https://{site}.com')

        # Get the current time
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, the time is {strTime}")

        # ---MODIFIED for Windows---: Open the Camera app
        elif "open camera" in query:
            say("Opening the camera.")
            os.system('start microsoft.windows.camera:')


        # Trigger the generative AI for complex queries
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Exit the program
        elif " quit" in query:
            say("Goodbye Sir")
            exit()

        # Reset the chat history
        elif "reset chat" in query:
            say("Resetting the chat history.")
            chat_session = model.start_chat(history=[])

        # Default to a chat session with Gemini
        else:
            print("Chatting...")
            try:
                # Use the chat session to send the message
                response = chat_session.send_message(query)
                say(response.text)
            except Exception as e:
                print(f"An error occurred during chat: {e}")
                say("I'm sorry, I'm having trouble responding right now.")