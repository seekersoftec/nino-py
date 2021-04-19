import os
import pandas as pd
# from googlesearch import search
from lib.constants import COMMON_MAIL_DOMAINS, ROLE_BASED_NAMES
from .scraper import get_info

# csv_file = os.getcwd()+"/data/generated_{0}.csv".format(length)
COMPRESSION = 'gzip'
AT_SYMBOL = '@'


def df_write(csv_file: str, dataframe):
    return dataframe.to_csv(csv_file, index=False, compression=COMPRESSION)


def df_read(csv_file: str):
    return pd.read_csv(csv_file, compression=COMPRESSION)


def add_domains(dataframe):
    #
    # combinations = ["".join(s) for s in combinations]
    # combinations.extend([first_name, last_name])
    # permuted_emails = [f"{s}@{domain_name}" for s in combinations]
    #
    for i in range(len(COMMON_MAIL_DOMAINS)):
        dataframe[COMMON_MAIL_DOMAINS[i].split('.')[0]] = dataframe['generated_strings'].apply(
            lambda x: "{0}{1}{2}".format(x, AT_SYMBOL, COMMON_MAIL_DOMAINS[i]))

    return dataframe

# def google_search(term, num_results = 75):
#     return search(term, num_results=num_results)


# def pbin_scraper():
#     terms = ['pastebin email address', '']
#     results = list(map(google_search, terms))
#     return results
