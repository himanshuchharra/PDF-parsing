#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import click
import os
import glob
import traceback
from bottle import Bottle, run, request, HTTPResponse
from constants import APP_HOST, APP_PORT, DIRECTORY
from REST.request import validate
from REST.response import error, http, success
from Converter import convert
from Parser import ParseBank
from Logger import error as error_logger
from Exception import ScannedPDFException, InvalidBankNameException


app = Bottle()


@app.route('/api/v1/health')
def health():
    return HTTPResponse(status=200, body='Healthy')


@app.route('/api/v1/analyser', method='POST')
def analyser():
    """
    Analyser analyse the bank statement
    Converter convert this into a xml
    Parser parse the xml and generates the data dictionary
    :return: HTTPResponse
    """
    errors = validate(request)
    if errors:
        return http(422, error(errors, 422))

    # Upload and save the incoming file to the temp directory
    upload = request.files.get('upload')
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # Generate the directory path for pdf and xml
    name, ext = os.path.splitext(upload.filename)
    directory_path = os.path.join(DIRECTORY, name)
    pdf_path = directory_path + '.pdf'
    xml_path = directory_path + '.xml'

    # Save the file
    upload.save(pdf_path, overwrite=True)

    try:
        # Converting the pdf into a xml and saving it into a temp directory
        convert(pdf_path, xml_path)

        # Initiate the parser to parse the xml and generate the data dictionary
        parsebank_obj = ParseBank()
        data = parsebank_obj.parse(xml_path)

    except InvalidBankNameException as exception:
        exp = dict(invalid_data=str(exception))
        return http(400, error(exp, 400))
    except ScannedPDFException as exception:
        exp = dict(resource_not_found=str(exception))
        return http(404, error(exp, 404))
    except Exception as exception:
        error_logger(traceback.format_exc())
        error_logger(str(exception))
        exp = dict(internal_server_error='Failed to analyse the bank statement')
        return http(500, error(exp, 500))
    finally:
        # Remove temp directory after getting transactions
        if os.path.exists('temp'):
            for filename in glob.glob(directory_path + "*"):
                os.remove(filename)

    return http(201, success(201, data, 'analyser'))


@click.command()
@click.option('--host', help='Host', default=APP_HOST)
@click.option('--port', help='Post', default=APP_PORT)
def start(host, port):
    run(app=app, host=host, port=port, reloader=True)


if __name__ == '__main__':
    start()
