#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import os
from dotenv import load_dotenv
from pathlib import Path

# Load the env file from the APP root directory
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APP_HOST = os.environ['APP_HOST']
APP_PORT = os.environ['APP_PORT']

LOG_PATH = os.environ.get('LOG_PATH', '.')

DIRECTORY = 'temp'

PDF_DESTINATION = 'temp/statement.pdf'
XML_DESTINATION = 'temp/statement.xml'