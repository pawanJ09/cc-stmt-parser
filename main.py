from PyPDF2.errors import PdfReadError
from PyPDF2._reader import PdfReader
from globals import expense_map
import re
import os

txn_start = '$ Amount'
txn_end = 'Total fees charged'


def generate_pdf_reader():
    """
    This method generates an instance of PDFReader and returns it back for the provided input
    file name
    :return: PDFReader reader
    """
    files = os.listdir('stmt')
    file_name = ''
    for f in files:
        # Fetch the first file
        file_name = 'stmt/'+f
        break
    file_obj = open(file_name, 'rb')
    reader = PdfReader(file_obj, strict=False)
    print(f'File being processed {file_name.split("/")[-1]}')
    return reader


def parse_transactions(reader: PdfReader):
    """
    This method reads all the pages from the provided reader, extracts the text and filters
    credit card transactions before adding them to a list and returning the list of transactions
    :param reader: PdfReader object
    :return: List of transactions
    """
    txn_found = False
    split_transactions = []
    for page_num in range(len(pdf_reader.pages)):
        try:
            page_content = pdf_reader.pages[page_num]
            transactions = page_content.extract_text()
            if (transactions.find(txn_start) > 0 and not txn_found) or txn_found:
                txn_found = True
                raw_transactions = transactions[transactions.find(txn_start) + len(txn_start):
                                                transactions.find(txn_end)]
                split_transactions.extend(raw_transactions.splitlines())
        except PdfReadError:
            txn_found = False
    return split_transactions


def categorize_transactions(transactions: list):
    expenses = dict()
    expenses_classified = dict()
    for txn in transactions:
        # Filter transactions which have a date and no negatives i.e. payments
        if re.findall("\d+\/\d+", txn) and not re.findall("-\d+\.\d+", txn) \
                and (re.findall("\d+\.\d+", txn) or re.findall("\.\d+", txn)):
            # Parsing the amount from txn using one of the formats as specified
            amount = re.findall("\d+\,\d+\.\d+", txn) or re.findall("\d+\.\d+", txn) \
                     or re.findall("\.\d+", txn)
            for expense_category, expense_values in expense_map.items():
                if any(val.lower() in txn.lower() for val in expense_values):
                    if expense_category not in expenses:
                        expenses_classified[expense_category] = list()
                        expenses[expense_category] = round(float(amount[0].replace(',', '')), 2)
                    else:
                        expenses[expense_category] = round(expenses[expense_category]
                                                           + float(amount[0].replace(',', '')), 2)
                    expenses_classified[expense_category].append(txn)
                    break
    print('\n')
    print('*'*50)
    print('DETAILED EXPENSES')
    print('*'*50)
    for category, txn in expenses_classified.items():
        print(category)
        [print(t) for t in txn]
    print('\n')
    print('*' * 50)
    print('TOTALED EXPENSES')
    print('*' * 50)
    print(expenses)



if __name__ == '__main__':
    pdf_reader = generate_pdf_reader()
    cc_transactions = parse_transactions(pdf_reader)
    categorize_transactions(cc_transactions)
