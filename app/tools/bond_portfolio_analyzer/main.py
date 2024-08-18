from . import utils
from .bond_portfolio import BondPortfolio
import logging
import os

# Current day prices are not available yet. Please try back after 1:00 p.m. EST.
# Remember to refresh your connection each time to get the most recent available information.
TREASURY_PRICES_URL = 'https://treasurydirect.gov/GA-FI/FedInvest/todaySecurityPriceDetail'

logger = logging.getLogger(__name__)

def rewrite_prev_closing_prices(http_response_text):
    with open(os.environ.get('BOND_CLOSING_PRICES_LOCATION'), 'w') as file:
        file.write(http_response_text)
    
def prepare_bonds_data(treasury_prices_url):
    response = utils.get_page(treasury_prices_url)
    text = utils.get_page_text(response)
    if 'Current day prices are not available yet.' in text:
        logger.info("Current day prices are not available yet from Treasury Direct. "
                    "Using previous day's data.")
        with open(os.environ.get('BOND_CLOSING_PRICES_LOCATION'), 'r') as file:
            text = file.read()
    else:
        rewrite_prev_closing_prices(text)
    soup = utils.soupify_text(text)
    table = utils.get_prices_table(soup)
    bonds_data = utils.separate_individual_bonds(soup)
    bond_dict = utils.make_bond_dict(bonds_data)
    return bond_dict

def calculate_portfolio_statistics(bond_portfolio: BondPortfolio):
    print(bond_portfolio.calculate_bond_portfolio_market_value())
    print(bond_portfolio.calculate_portfolio_duration())
    mod_d = bond_portfolio.calculate_portfolio_duration(modified=True)
    print(mod_d)
    print(bond_portfolio.calculate_portfolio_dv01(mod_d))

