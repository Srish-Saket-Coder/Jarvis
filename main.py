import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
import datetime
import json
import requests
from api_keys import openai_api_key, weather_api_key


speaker = win32com.client.Dispatch('SAPI.SpVoice')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f'User said: {query}')
            return query
        except Exception as e:
            return "Some error Occurred. Sorry from Jarvis"


def ai(query):
    openai.api_key = openai_api_key
    text = f'OpenAi response for Prompt: {query} \n ******************************* \n\n'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("openai"):
        os.mkdir("openai")

    # with open(f"openai/prompt - {random.randint(1, 34565789897654)}", 'w') as f:
    with open(f"openai/{''.join(query.split('intelligence')[1:]).strip()}.txt", 'w') as f:
        f.write(text)
    # todo: write this inside the try catch block


chatstr = ''


def chat(query):
    global chatstr
    # write a program to use open ai
    openai.api_key = openai_api_key
    chatstr += f'Srish: {query}\n Jarvis: '
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speaker.speak(response["choices"][0]["text"])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
    # if not os.path.exists("openai"):
    #     os.mkdir("openai")

    # # with open(f"openai/prompt - {random.randint(1, 34565789897654)}", 'w') as f:
    # with open(f"openai/{''.join(query.split('intelligence')[1:]).strip()}.txt", 'w') as f:
    #     f.write(text)


def weather(query):
    api_key = weather
    query = ''.join(query.split('in')[1:]).strip()
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={query}"
    data = json.loads(requests.get(base_url).text)
    print(data)
    return data.get('current').get('temp_c'), query


if __name__ == "__main__":
    speaker.speak("Hello, I am Jarvis AI")

    while True:
        print('Listening...')
        query = take_command()
        sites = [['youtube', 'https://www.youtube.com/'], ['wikipedia', 'https://www.wikipedia.com/'],
                 ['google', 'https://www.google.com/'], ['chat gpt', 'https://chat.openai.com']]
        for site in sites:
            if f'Open {site[0]}'.lower() in query.lower():
                speaker.speak(f"Opening {site[0]} Sir")
                webbrowser.open(site[1])

        if 'weather'.lower() in query.lower():
            print('Getting Weather...')
            weather = weather(query)
            print(f'Weather is {weather}')
            speaker.speak(f'Weather is {weather[0]} in {weather[1]}')
        elif f'the time'.lower() in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minutes = datetime.datetime.now().strftime("%M")

            speaker.speak(f"Sir the time is {hour} hour {minutes} minute")
        elif f'file explorer'.lower() in query.lower():
            speaker.speak(f"Opening File explorer Sir")
            os.system('explorer.exe')
        elif "artificial intelligence".lower() in query.lower():
            ai(query)
        elif 'reset'.lower() in query.lower():
            chatstr = ''
            speaker.speak("Reseting Chat")
        elif "quit" in query.lower():
            speaker.speak("Shutting down Jarvis")
            exit()
        else:
            print('Chatting...')
            chat(query)

        # speaker.speak(query)
