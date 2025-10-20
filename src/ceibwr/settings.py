# settings.py
# TODO base_settings.py, dev_settings.py, prod_settings.py

# old style
# import os
# data_path = os.path.join(os.path.dirname(__file__), 'data', 'data1.txt')
# with open(data_path, 'r') as data_file:
#
# new style
# from importlib.resources import files
# data_text = files('mypkg.data').joinpath('data1.txt').read_text()

import os
import json

# python <=3.9
# from importlib_resources import files

# python >=3.10
from importlib.resources import files

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_ROOT = os.path.dirname(PACKAGE_ROOT)
PROJECT_ROOT = os.path.dirname(SRC_ROOT)

# PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
# PROJECT_ROOT = os.path.path('Users/scmde/ceibwr/')
# PACKAGE_ROOT = os.path.dirname(PROJECT_ROOT, 'src')

# SRC_ROOT = os.path.dirname(os.path.abspath(__file__))

# CERDDI_ROOT = os.path.join(PROJECT_ROOT, 'data/cerddi')

LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')
LOG_FILE_NAME = os.path.join(LOG_ROOT, 'ceibwr.log')

# PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(SRC_ROOT, 'data')
# DATABASES = {
#     'default': {
#         'ODLIADUR': os.path.join(DATA_ROOT, 'odliadurRS.json'),
#         'GEIRFA': os.path.join(DATA_ROOT, 'geiriauJGJ.txt'),
#     }
# }

# data_text = files('mypkg.data').joinpath('data1.txt').read_text()

# miniJGJ = files('ceibwr.data').joinpath('miniJGJ.txt').read_text()
# miniJGJ = miniJGJ.strip().split(os.linesep)

geirfaJGJ = files('ceibwr.data').joinpath('geirfaJGJ.txt').read_text()
geirfaJGJ = geirfaJGJ.strip().split(os.linesep)

odliadur_file = files('ceibwr.data').joinpath('odliadurRS.json')
with open(odliadur_file, "r") as infile:
    odliadurRS = json.load(infile)

GEIRIADURON = {
    'default': {
        'GEIRFA': geirfaJGJ,
        # 'GEIRFA': geirfaJGJ,
        'ODLIADUR': odliadurRS,
    }
}

# print(odliadurRS)
# print(type(odliadurRS))