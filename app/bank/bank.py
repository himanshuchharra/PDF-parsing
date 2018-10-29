class Bank(object):
    """
    Parent class for different banks
    """
    bank_details = {'bank_name': '', 'name': '', 'account_number': '', 'opening_balance': '',
                        'closing_balance': '', 'from_date': '', 'to_date': '', 'currency': '',  'transactions': []}

    def coordinates_position(self, find, page_width, text_tag):
        """
        Searches for the parameters of columns in transaction in a xml
        :param find: int
        :param page_width: int
        :param text_tag: string
        :return: left: int, right: int
        """
        if "Date" in text_tag[find].text:
            left = 0
            right = int(text_tag[find + 1].get("left"))
            return left, right
        elif "Balance ($)" in text_tag[find].text:
            left = int(text_tag[find - 1].get("left")) + int(text_tag[find - 1].get("width"))
            right = page_width
            return left, right
        else:
            left = int(text_tag[find - 1].get("left")) + int(text_tag[find - 1].get("width"))
            right = int(text_tag[find + 1].get("left"))
            return left, right
