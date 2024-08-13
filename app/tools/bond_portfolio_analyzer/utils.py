import requests
from bs4 import BeautifulSoup
import re
import datetime

def get_page(url):
    return requests.get(url)

def get_page_text(response_obj):
    return response_obj.text


def soupify_text(html):
    return BeautifulSoup(html, 'html.parser')


def get_prices_table(soup):
    return soup.find('table', {'class': 'data1'})


def separate_individual_bonds(bond_table):
    return bond_table.find_all('tr')

def _transform_maturity_datetime(date_str):
    dt = datetime.datetime.strptime(date_str, '%M/%d/%Y')
    return dt.strftime('%Y-%M-%d')

def calculate_cumulative_pnl(portfolio, bond_dict):
    pnl_dict = {}
    for bond in portfolio:
        pnl_dict[bond.cusip] = round((bond_dict[bond.cusip]['mid_price'] -
                                      float(bond.purchase_price)) * (int(bond.notional) / 100), 2)
    return pnl_dict

def _calculate_mid(bid, ask):
    if float(bid) == 0.0 and float(ask) > 0.0:
        return float(ask)
    elif float(bid) > 0.0 and float(ask) == 0.0:
        return float(bid)
    elif float(bid) > 0.0 and float(ask) > 0.0:
        return round((float(bid) + float(ask)) / 2, 2)

def make_bond_dict(individual_bonds):
    bond_dict = {}
    for bond in individual_bonds:
        attributes = bond.find_all('td')
        if attributes:
            if re.match(r'\w{9}', attributes[0].text):
                cusip = attributes[0].text
                security_type = attributes[1].text
                coupon = attributes[2].text
                maturity_date = _transform_maturity_datetime(attributes[3].text)
                call_date = attributes[4].text
                bid_price = attributes[5].text
                ask_price = attributes[6].text
                mid_price = _calculate_mid(bid_price, ask_price)
                end_of_day = attributes[7].text
                bond_dict[cusip] = {
                                    'security_type': security_type,
                                    'coupon': coupon,
                                    'maturity_date': maturity_date,
                                    'call_date': call_date,
                                    'bid_price': bid_price,
                                    'ask_price': ask_price,
                                    'mid_price': mid_price,
                                    'end_of_day': end_of_day
                                    }
    return bond_dict
