#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import json
from bottle import HTTPResponse


# def error(errors):
#     """
#     Generate the error response
#     :param errors:
#     :return: HTTPResponse
#     """
#     response = {'status': 'failed', 'code': '422', 'errors': {}}
#
#     list_of_errors = {}
#     for key, value in errors.items():
#         list_of_errors[key] = [value]
#
#     response['errors'] = list_of_errors
#
#     return HTTPResponse(status=422, body=json.dumps(response),
#                         headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})


def error(errors, code):
    """
    Generate the error response
    :param errors:
    :param code:
    :return:
    """
    response = {'status': 'failed', 'code': code, 'errors': {}}

    list_of_errors = {}
    for key, value in errors.items():
        list_of_errors[key] = [value]

    response['errors'] = list_of_errors

    return response


def http(status, body):
    return HTTPResponse(status=status, body=body,
                        headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})


def success(code, data, resource):
    response = {'status': 'success', 'code': code, 'data': data, 'resource': resource}
    return response


# def success(status_code, data, resource):
#     """
#     Generate the success response
#     :param status_code:
#     :param data:
#     :param resource:
#     :return:
#     """
#     response = {'status': 'success', 'code': status_code, 'data': data, 'resource': resource}
#     return HTTPResponse(status=status_code, body=json.dumps(response),
#                         headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'})
