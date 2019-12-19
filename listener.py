from skype_chatbot import skype_chatbot
import time
import requests
from requests.exceptions import ConnectionError

app_id = '5a8a1b2b-2f04-4eb9-818c-5023d5c6ba4e'
app_secret = 'h-J8h]:ho=ooI6lGRIenn2UzzZ1ZORAx'
secret = 'XDxlsiASYxU.CRV44VKDG_WIrIPLEdk5ygJPWMSjq-CjLCnbQ0tiYGs'

bot = skype_chatbot.SkypeBot(app_id, app_secret)
sender = '19:74deadbfd1dd43af8fda0e0d4eb6728f@thread.skype'
recipient = ''
service = 'https://smba.trafficmanager.net/apis/'
text = 'test'
text_format = 'markdown'


gv_ms4 = 'http://ukdcwl12cgvdev.vistajet.local:7006/VJET/index.html'
is_down = None

def get_errno(reason):
    import re
    splitted = re.split('\[', reason)
    splitted = re.split('\]', splitted[-1])
    splitted = re.split(' ', splitted[0])
    return int(splitted[-1])

while(True):
    print('Checking GV...')
    try:
        re = requests.get('http://ukdcwl12cgvdev.vistajet.local:7006/VJET/index.html')
        if is_down and re.status_code == 200:
            print('GV MS4 is Up')
            is_down = False
            bot.send_message(app_id, 'Debtors bot', recipient, service, sender, 'No', text_format)
        elif not is_down and re.status_code != 200:
            print('GV MS4 is Down')
            is_down = True
            bot.send_message(app_id, 'Debtors bot', recipient, service, sender, 'Yes', text_format)
        else:
            print('No changes')
    except ConnectionError as e:
        errno = get_errno(str(e))
        if is_down != (errno == 111):
            print('GV MS4 is Down')
            is_down = True
            # bot.send_message(app_id, 'Debtors bot', recipient, service, sender, 'Yes', text_format)
        else:
            print('No changes')
    finally:
        time.sleep(60 * 5)
