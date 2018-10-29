#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import os


def validate(request):
    """
    The validate method will validate the incoming request against the request parameters
    :param request:
    :return: dictionary
    """
    upload = request.files.get('upload', None)
    if upload is None:
        return {'upload': "PDF file is required"}

    name, ext = os.path.splitext(upload.filename)
    if ext not in '.pdf' or not ext:
        return {'upload': "Supported format for this request is PDF"}
