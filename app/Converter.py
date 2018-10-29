#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import subprocess
import traceback
from Logger import error as error_logger


def convert(file, path):
    """
    Extract the contents from a pdf and converts it into xml and save it to a path
    :param file: string
    :param path: string
    :return: bool
    """
    try:
        process = subprocess.Popen(['pdftohtml -c -nodrm -hidden -xml ' + file + ' ' + path], shell=True)
        process.wait()
    except Exception as exception:
        error_logger(traceback.format_exc())
        error_logger(str(exception))

