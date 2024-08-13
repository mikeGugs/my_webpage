from app.auth import auth_bp
from flask import Flask, render_template, url_for, request, redirect, session, flash, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.extensions import db
from app.forms.forms import LoginForm, SignUpForm, AddBondsForm
from flask_login import login_required, current_user, login_user, logout_user
from app.tools.bond_portfolio_analyzer.bond_portfolio import BondPortfolio
from app.tools.bond_portfolio_analyzer.utils import calculate_cumulative_pnl
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from app.tools.bond_portfolio_analyzer.main import prepare_bonds_data, TREASURY_PRICES_URL

@auth_bp.route('/login')
def login():
    form = LoginForm()    
    return render_template('login.html', form=form)

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login credentials and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    return redirect(url_for('auth.profile'))

@auth_bp.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    # NEED TO MAKE THIS PAGE SHOW CORRECT ERRORS
    username = request.form.get('username')
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        flash('username already exists. please try a different one.')
        return redirect(url_for('auth.signup'))

    new_user = User(username=username,
                    email_address=email,
                    fullname=full_name,
                    password=generate_password_hash(password, method='pbkdf2:sha256')
                    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.profile'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/bond_portfolio_analysis')
@login_required
def bond_portfolio_analysis():
    cur_user = current_user.username
    load_dotenv()
    engine = create_engine(os.environ.get('DATABASE_LOCATION'))
    session = Session(engine)
    prev_closing_prices = os.environ.get('BOND_CLOSING_PRICES_LOCATION') # NEED TO UPDATE THIS IN DOTENV IN PRODUCTION
    bond_data = prepare_bonds_data(TREASURY_PRICES_URL, prev_closing_prices)
    bp = BondPortfolio(bond_data, session, cur_user)
    matured_message = bp.clean_matured_bonds()
    if type(matured_message) == list:
        for message in matured_message:
            flash(message)
    current_holdings = bp.get_current_portfolio_holdings()
    pnl_dict = calculate_cumulative_pnl(current_holdings, bond_data)
    market_value = bp.calculate_bond_portfolio_market_value()
    mac_dur = bp.calculate_portfolio_duration()
    mod_dur = bp.calculate_portfolio_duration(modified=True)
    dv01 = bp.calculate_portfolio_dv01(mod_dur)
    tot_pnl = sum(list(pnl_dict.values()))

    return render_template('bond_portfolio_analysis.html',
                           bonds = current_holdings,
                           username = cur_user,
                           bond_info_dict = bond_data,
                           pnl_dict = pnl_dict,
                           market_value=market_value,
                           mac_dur=mac_dur,
                           mod_dur=mod_dur,
                           dv01=dv01,
                           tot_pnl=tot_pnl
                           )

@auth_bp.route('/add_bonds')
@login_required
def add_bonds():
    form = AddBondsForm()

    cur_user = current_user.username
    load_dotenv()
    engine = create_engine(os.environ.get('DATABASE_LOCATION'))
    session = Session(engine)
    prev_closing_prices = os.environ.get('BOND_CLOSING_PRICES_LOCATION') # NEED TO UPDATE THIS IN DOTENV IN PRODUCTION
    bond_data = prepare_bonds_data(TREASURY_PRICES_URL, prev_closing_prices)
    bp = BondPortfolio(bond_data, session, cur_user)
    current_holdings = bp.get_current_portfolio_holdings()
    pnl_dict = calculate_cumulative_pnl(current_holdings, bond_data)
    
    return render_template('add_bonds.html',
                           form=form,
                           username=cur_user,
                           bonds=current_holdings,
                           bond_info_dict=bond_data,
                           pnl_dict=pnl_dict
                           )

@auth_bp.route('/add_bonds', methods=['POST'])
@login_required
def add_bonds_post():
    cur_user = current_user.username
    load_dotenv()
    engine = create_engine(os.environ.get('DATABASE_LOCATION'))
    session = Session(engine)
    prev_closing_prices = os.environ.get('BOND_CLOSING_PRICES_LOCATION') # NEED TO UPDATE THIS IN DOTENV IN PRODUCTION
    bond_data = prepare_bonds_data(TREASURY_PRICES_URL, prev_closing_prices)
    bp = BondPortfolio(bond_data, session, cur_user)
    cusip = request.form.get('cusip')
    notional = int(request.form.get('notional'))
    purchase_price = float(request.form.get('purchase_price'))

    poss_message = bp.add_bond(cusip, notional, purchase_price)
    if type(poss_message) == str:
        flash(poss_message)

    return redirect(url_for('auth.add_bonds'))

@auth_bp.route('/remove_bonds')
@login_required
def remove_bonds():
    cur_user = current_user.username
    load_dotenv()
    engine = create_engine(os.environ.get('DATABASE_LOCATION'))
    session = Session(engine)
    prev_closing_prices = os.environ.get('BOND_CLOSING_PRICES_LOCATION') # NEED TO UPDATE THIS IN DOTENV IN PRODUCTION
    bond_data = prepare_bonds_data(TREASURY_PRICES_URL, prev_closing_prices)
    bp = BondPortfolio(bond_data, session, cur_user)
    current_holdings = bp.get_current_portfolio_holdings()
    pnl_dict = calculate_cumulative_pnl(current_holdings, bond_data)

    return render_template('remove_bonds.html',
                           username=cur_user,
                           bonds=current_holdings,
                           bond_info_dict=bond_data,
                           pnl_dict=pnl_dict
                           )

@auth_bp.route('/remove_bonds', methods=['POST'])
@login_required
def remove_bonds_post():
    cur_user = current_user.username
    load_dotenv()
    engine = create_engine(os.environ.get('DATABASE_LOCATION'))
    session = Session(engine)
    prev_closing_prices = os.environ.get('BOND_CLOSING_PRICES_LOCATION') # NEED TO UPDATE THIS IN DOTENV IN PRODUCTION
    bond_data = prepare_bonds_data(TREASURY_PRICES_URL, prev_closing_prices)
    bp = BondPortfolio(bond_data, session, cur_user)
    to_remove = request.form.getlist('to_remove')
    for id in to_remove:
        bp.remove_bond(id)

    return redirect(url_for('auth.remove_bonds'))
