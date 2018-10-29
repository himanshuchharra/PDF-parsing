#!/usr/bin/env python
# coding: utf-8

# Madhur Tandon, Biz2Credit

import re
from datetime import datetime
from app.bank.bank import Bank


class ParseBMO(Bank):
    def parse_bmo(self, page_tag, bank_name):
        """
        Parse the xml and create a data dictionary
        :param page_tag: Content of all pages
        :param bank_name: Name of Bank
        :return: list[dict]
        """

        details_tag = page_tag[0].find_all('text')
        details_tag_count = len(details_tag)
        style = []
        skip = 10
        transacts = []
        bank_obj = Bank()
        bank_obj.bank_details['bank_name'] = bank_name

        for iterText in range(details_tag_count):
            if int(details_tag[iterText].get("left")) < 150 < int(details_tag[iterText].get("top")) < 300:
                style.append(details_tag[iterText].get("height"))
            if "business account" in details_tag[iterText].text.lower():
                bank_obj.bank_details['account_number'] = re.sub('[a-z A-Z#]', '', details_tag[iterText].text)
            if "business banking statement" in details_tag[iterText].text.lower():
                bank_obj.bank_details['currency'] = "Canadian Dollar"
                period = details_tag[iterText + 1].text

        name_style = max(style, key=style.count)
        for iterText in range(details_tag_count):
            if int(details_tag[iterText].get("left")) < 150 < int(details_tag[iterText].get("top")) < 300 and details_tag[iterText].get("height")== name_style :
                bank_obj.bank_details['name'] = details_tag[iterText].text
                break

        to_date = period.split()[-3::]
        to_date = ' '.join(to_date)
        to_date = datetime.strptime(to_date, "%B %d, %Y")
        bank_obj.bank_details['from_date'] = '01' + to_date.strftime('/%m/%Y')
        bank_obj.bank_details['to_date'] = to_date.strftime('%d/%m/%Y')

        # Extract Transaction information from each page
        for iterPage in range(len(page_tag)):
            text_tag = page_tag[iterPage].find_all('text')
            page_width = int(page_tag[iterPage].get("width"))
            text_tag_count = len(text_tag)

            for iterText in range(text_tag_count):
                if "transaction details" in text_tag[iterText].text.lower():
                    start_find = iterText
                    break

            if 'start_find' in locals():
                date_text_left, date_text_right = bank_obj.coordinates_position(start_find + 3, page_width, text_tag)
                description_text_left, description_text_right = bank_obj.coordinates_position(start_find + 4, page_width, text_tag)
                debit_text_left, debit_text_right = bank_obj.coordinates_position(start_find + 5, page_width, text_tag)
                credit_text_left, credit_text_right = bank_obj.coordinates_position(start_find + 6, page_width, text_tag)
                single_transaction = {'date': '', 'description': '', 'type': '', 'amount': '', 'balance': ''}

                for dateIter in range((start_find + skip), text_tag_count):
                    if text_tag[dateIter].text == ' ':
                        continue
                    if text_tag[dateIter].text == "Closing totals":
                        break
                    if 'transaction_style' in locals():
                        if int(transaction_style) - int(text_tag[dateIter].get("top")) > 100 or int(text_tag[dateIter].get("top")) - int(transaction_style) > 40:
                            break
                    if text_tag[dateIter].text == 'Opening balance':
                        balance = float(re.sub('[$,]', '', text_tag[dateIter + 1].text))
                        bank_obj.bank_details['opening_balance'] = balance

                    left = int(text_tag[dateIter].get("left"))
                    right = left + int(text_tag[dateIter].get("width"))

                    if left > date_text_left and right < date_text_right:
                        date = text_tag[dateIter].text
                        single_transaction['date'] = date

                    elif left > description_text_left and right < description_text_right:
                        single_transaction['description'] = single_transaction['description'] + (text_tag[dateIter].text + ' ')
                        transaction_style = text_tag[dateIter].get("top")

                    elif left > debit_text_left and right < debit_text_right:
                        debit_amount = text_tag[dateIter].text
                        debit_amount = float(re.sub('[$,]', '', debit_amount))
                        balance = float(balance - debit_amount)
                        balance = round(balance, 2)
                        single_transaction['type'] = 'DR'
                        single_transaction['amount'] = debit_amount
                        single_transaction['balance'] = balance
                        closing_balance = balance
                        transacts.append(single_transaction)
                        single_transaction = {'date': '', 'description': '', 'type': '', 'amount': '', 'balance': ''}
                    elif left > credit_text_left and right < credit_text_right:
                        credit_amount = text_tag[dateIter].text
                        credit_amount = float(re.sub('[$,]', '', credit_amount))
                        balance = float(balance + credit_amount)
                        balance = round(balance, 2)
                        single_transaction['type'] = 'CR'
                        single_transaction['amount'] = credit_amount
                        single_transaction['balance'] = balance
                        closing_balance = balance
                        transacts.append(single_transaction)
                        single_transaction = {'date': '', 'description': '', 'type': '', 'amount': '', 'balance': ''}
                del transaction_style
                del start_find
            skip = 9

        bank_obj.bank_details['closing_balance'] = closing_balance
        bank_obj.bank_details['transactions'] = transacts
        bank_details = bank_obj.bank_details
        return bank_details
