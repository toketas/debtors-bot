from skype_chatbot import skype_chatbot
import time
import requests
import logging
from requests.exceptions import ConnectionError

app_id = '5a8a1b2b-2f04-4eb9-818c-5023d5c6ba4e'
app_secret = 'h-J8h]:ho=ooI6lGRIenn2UzzZ1ZORAx'
secret = 'XDxlsiASYxU.CRV44VKDG_WIrIPLEdk5ygJPWMSjq-CjLCnbQ0tiYGs'

bot = skype_chatbot.SkypeBot(app_id, app_secret)

# old conversation id. Any changes on config will generate a new id
sender = '19:74deadbfd1dd43af8fda0e0d4eb6728f@thread.skype'
sender = '19:378331839ef04d738cec070ade0abacc@thread.skype'

recipient = ''
service = 'https://smba.trafficmanager.net/apis/'
text = 'test'
text_format = 'markdown'

logging.basicConfig(format='%(asctime)s %(message)s')

GV_ENVS = {
    'MS4': 'http://ukdcwl12cgvdev.vistajet.local:7006/VJET/index.html',
    'QA': 'http://ukdcapacheuat01.vistajet.local/VJET',
    'UAT': 'http://bpmtestpatch.vistajet.local:7003/VJET',
}

IS_DOWN_ENVS = {
    'MS4': None,
    'QA': None,
    'UAT': None,
}

def get_errno(reason):
    import re
    splitted = re.split('\[', reason)
    splitted = re.split('\]', splitted[-1])
    splitted = re.split(' ', splitted[0])
    return int(splitted[-1])

def check_gv_env_is_down(env):
    try:
        re = requests.get(GV_ENVS[env])
        return re.status_code != 200
    except ConnectionError as e:
        errno = get_errno(str(e))
        return errno == 111

def get_status_text(envs):
    result_text = """"""
    for key in envs.keys():
        result_text += "GV {} - *{}* \n".format(key, 'DOWN' if IS_DOWN_ENVS[key] else 'UP')

    return result_text

while(True):
    logging.warning('Checking GV...')
    has_changes = False
    for key in GV_ENVS.keys():
        is_down = check_gv_env_is_down(key)
        if is_down != IS_DOWN_ENVS.get(key, None):
            has_changes = True
            logging.warning("GV {} is {}".format(key, 'Down' if is_down else 'Up'))
            IS_DOWN_ENVS[key] = is_down
    if has_changes:
        text = get_status_text(IS_DOWN_ENVS)
        bot.send_message(app_id, 'Debtors bot', recipient, service, sender, text, text_format)
    else:
        logging.warning('No changes')
    # Wait 5 minutes
    time.sleep(60 * 5)
