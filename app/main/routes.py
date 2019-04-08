
from flask import render_template, url_for, request, redirect
from flask_login import login_required
from flask_login import current_user
from . import bp
from ..models import Model as DBHelper
from .utils import BitlyHelper
from config import Config

DB = DBHelper()
BH = BitlyHelper()

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/account')
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template('account.html', tables=tables)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/account/createtable', methods=('POST','GET'))
@login_required
def account_createtable():
    tablename = request.form.get('tablenumber')
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = Config.BASE_URL + "newrequest/" + tableid
    new_url = BH.shorten_url(new_url)
    print(new_url)
    DB.update_table(tableid, new_url)
    return redirect(url_for('main.account'))

@bp.route('/account/deletetable')
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('main.account'))

