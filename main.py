import requests
import json
import time

from pypresence import Presence

state = 0
def status(token, messages):

    global state
    prompt = ''

    try:
        response = requests.patch(
            url='https://discord.com/api/v10/users/@me/settings', headers={'authorization': token},
            json={'custom_status': {'text': messages[state]['Message'], 'emoji_id': messages[state]['Emoji_ID']}})
        if response.status_code == 200:
            prompt = f'\033[35mSUCCESS | Successfully changed status. ({messages[state]})\033[0m'
        else:
            prompt = f'\033[31mERROR | Couldnt change status.\033[0m'
    except Exception as error:
        prompt = f'\033[31mERROR | Couldnt change status: {error}.\033[0m'

    state += 1
    if len(messages) <= state:
        state = 0

    return prompt

def presence(client, settings):

    try:
        
        buttons = []
        for i in settings['Buttons']: buttons.append(i)

        connection = Presence(client)
        connection.connect()
        connection.update( state=settings['Title'], details=settings['Details'], large_image=settings['Image'], small_image=settings['Image'],
            start=int(time.time()) - (settings['Start'] * 365 * 24 * 60 * 60),
            buttons=buttons if len(buttons) > 0 else None)
        
        print(f'\033[35mSUCCESS | Successfully created connection with presence.')
    except Exception as error:
        print(f'\033[31mERROR | Couldnt create connection with presence: {error}.')
        return

def main():
    
    def config():
        try:
            with open('config.json', 'r') as book:
                data = json.load(book)
                return data
            return
        except:
            return

    settings = config()

    if not settings: return
    else: settings = settings['Config']

    if not (settings['Token'] and (settings['Client'] or settings['Client'] == "") and len(settings['Messages']) > 0): return
    if (settings['Presence'] and settings['Client'] != ""): presence(settings['Client'], settings['Presence'])

    while True:
        time.sleep(5) ## havent tested less cooldown, try at your own risk
        response = status(settings['Token'], settings['Messages'])
        print(response)

main()
input() ## so cmd prompt doesnt close itself