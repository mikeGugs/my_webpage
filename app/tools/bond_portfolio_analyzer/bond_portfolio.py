import datetime
import bond_pricing
from app.models import User, Bonds
from functools import cache
from sqlalchemy import select, delete
import logging


class BondPortfolio:

    logger = logging.getLogger(__name__)

    def __init__(self, bond_closing_prices: dict, session, username: str):
        self.bond_closing_prices = bond_closing_prices
        self.session = session
        self.username = username

    @cache
    def _get_user_session(self):
        return self.session.get(User, self.username)

    def add_bond(self, cusip: str, notional: int, purchase_price: float):
        """type is discount or coupon"""
        if cusip in self.bond_closing_prices.keys()\
                and type(notional) == int and \
                (type(purchase_price) == int or type(purchase_price) == float):
            user_session = self._get_user_session()
            user_session.bonds.append(Bonds(cusip=cusip,
                                            notional=notional,
                                            purchase_price=purchase_price)
                                      )
            self.session.commit()
            return None

        elif cusip not in self.bond_closing_prices.keys():
            return (f"{cusip} does not exist in the pricing table from Treasury Direct! \n"
                  "This could be because it's a new issue, or there's a typo in the CUSIP entered.")
        else:
            return f"Unable to add {cusip} for unknown reason. Please check your inputs, and try again"

    def remove_bond(self, bond_id):
        to_delete = self.session.scalars(select(Bonds).where(
            Bonds.id == bond_id,
                                )).first()
        self.session.delete(to_delete)
        self.session.commit()

    def clean_matured_bonds(self):
        matured_messages = []
        today = datetime.datetime.today()
        for bond in self.get_current_portfolio_holdings():
            if today >= datetime.datetime.strptime(self.bond_closing_prices[bond.cusip]['maturity_date'], '%Y-%m-%d'):
                self.remove_bond(bond.id)
                matured_messages.append(f"{bond.cusip} has matured! Removed this from your current holdigs")
        if matured_messages:
            return matured_messages
        else:
            return None
            

    def get_current_portfolio_holdings(self):
        session = self._get_user_session()
        return [bond for bond in session.bonds]

    @staticmethod
    def _calculate_tplus_one_settle():
        today = datetime.datetime.today()
        if today.isoweekday() == 5:
            # Friday
            t_plus_one = today + datetime.timedelta(days=3)
        elif today.isoweekday() == 6:
            # Saturday
            t_plus_one = today + datetime.timedelta(days=2)
        else:
            t_plus_one = today + datetime.timedelta(days=1)
        return t_plus_one.strftime('%Y-%m-%d')

    def _get_current_bond_price(self, cusip):
        if cusip not in self.bond_closing_prices.keys():
            self.logger.warning(f"{cusip} does not exist on the Treasury Direct website! "
                                f"Maybe it's a new issue? Skipping.")
            return None
        bid_price = float(self.bond_closing_prices[cusip]['bid_price'])
        ask_price = float(self.bond_closing_prices[cusip]['ask_price'])
        if bid_price and not ask_price:
            return bid_price
        if ask_price and not bid_price:
            return ask_price
        if bid_price and ask_price:
            return (float(self.bond_closing_prices[cusip]['bid_price']) +
                    float(self.bond_closing_prices[cusip]['ask_price'])) / 2

    def calculate_ytm(self, cusip):
        if cusip not in self.bond_closing_prices.keys():
            self.logger.warning(f"{cusip} does not exist on the Treasury Direct website! "
                                f"Maybe it's a new issue? Skipping.")
            return None
        cpn = float(self.bond_closing_prices[cusip]['coupon'].rstrip('%'))/100
        mat = self.bond_closing_prices[cusip]['maturity_date']
        price = self._get_current_bond_price(cusip)
        if price:
            settle = self._calculate_tplus_one_settle()
            return bond_pricing.bond_yield(settle=settle, cpn=cpn, mat=mat,
                                           price=price, freq=2, comp_freq=2,
                                           face=100)

    def calculate_duration(self, cusip, ytm, modified=False):
        cpn = float(self.bond_closing_prices[cusip]['coupon'].rstrip('%'))/100
        mat = self.bond_closing_prices[cusip]['maturity_date']
        settle = self._calculate_tplus_one_settle()
        return bond_pricing.bond_duration(settle=settle, cpn=cpn, mat=mat,
                                          freq=2, yld=ytm, comp_freq=2, face=100,
                                          modified=modified)

    def calculate_dv01(self, cusip, modified_duration):
        """
        DV01 of current position in bond portfolio of specified CUSIP
        In this case, otherwise known as "money duration" of the bond
        """
        amt = self.session.scalars(
            select(Bonds.notional).where(
                Bonds.cusip == cusip, Bonds.user_id == self.username)).first()
        price = self._get_current_bond_price(cusip)
        if price:
            return (price / 100) * amt * modified_duration * .0001

    def calculate_bond_portfolio_market_value(self):
        market_value = 0
        user_session = self._get_user_session()
        for bond in user_session.bonds:
            price = self._get_current_bond_price(bond.cusip)
            if price:
                market_value += (price / 100) * bond.notional
        return round(market_value, 2)

    def calculate_portfolio_duration(self, modified=False):
        total_portfolio_value = self.calculate_bond_portfolio_market_value()
        user_session = self._get_user_session()
        total_dur = 0
        for bond in user_session.bonds:
            ytm = self.calculate_ytm(bond.cusip)
            if ytm:
                dur = self.calculate_duration(bond.cusip, ytm, modified)
                position = bond.notional
                price = self._get_current_bond_price(bond.cusip)
                if price:
                    total_dur += (((price / 100) * position) / total_portfolio_value) * dur
        return round(total_dur, 2)

    def calculate_portfolio_dv01(self, portfolio_mod_dur):
        mkt_value = self.calculate_bond_portfolio_market_value()
        return round(mkt_value * portfolio_mod_dur * .0001, 2)
