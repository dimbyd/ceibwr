# settings.py

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')

CERDDI_ROOT = os.path.join(PROJECT_ROOT, 'data/cerddi')
LOG_FILE_NAME = os.path.join(LOG_ROOT, 'ceibwr.log')

ADMINS = (
    ('dimbyd', 'evansd8@cf.ac.uk'),
)

DATABASES = {
    'default': {
        'ODLIADUR': os.path.join(DATA_ROOT, 'static/odliadurRS.json'),
        'GEIRFA': os.path.join(DATA_ROOT, 'static/geiriauJGJ.txt'),
    }
}
