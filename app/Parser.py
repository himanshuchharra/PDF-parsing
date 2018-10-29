#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import os
from bs4 import BeautifulSoup
from app.bank.parser_bmo import ParseBMO
from app.bank.parser_rbc import ParseRBC
from Exception import ScannedPDFException, InvalidBankNameException
from Logger import error as error_logger


class ParseBank(object):
    def parse(self, file):
        """
            Parse the xml and create a data dictionary
            :param file: xml file path
            :return: list[dict]
        """

        # Check if we are able to parse the pdf
        if not os.path.exists(file):
            raise ScannedPDFException('Scanned PDF are not supported')

        soup = BeautifulSoup(open(file), "lxml")
        page_tag = soup.find_all('page')
        details_tag = page_tag[0].find_all('text')
        details_tag_count = len(details_tag)

        if details_tag_count == 0:
            raise ScannedPDFException('Scanned PDF are not supported')

        bank_name = None
        for iterText in range(details_tag_count):
            error_logger(details_tag[iterText].text.lower())
            if "www.bmo.com" in details_tag[iterText].text.lower():
                bank_name = 'BANK OF MONTREAL'
                bmo_obj = ParseBMO()
                return bmo_obj.parse_bmo(page_tag, bank_name)
            elif "royal bank of canada" in details_tag[iterText].text.lower():
                bank_name = 'ROYAL BANK OF CANADA'
                rbc_obj = ParseRBC()
                return rbc_obj.parse_rbc(page_tag, bank_name)

        if bank_name is None:
            raise InvalidBankNameException('Only support parsing of the listed banks')
