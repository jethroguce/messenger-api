import os

BIND_IP = '127.0.0.1'
BIND_PORT = 5000


try:
    DEBUG = os.environ['DEBUG']

    if str.upper(DEBUG) == 'TRUE':
        DEBUG = True
    else:
        DEBUG = False
except:
    DEBUG = False

print('DEBUG Status ' + str(DEBUG))


FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
