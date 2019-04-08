import datetime
from flask import render_template, url_for, request, redirect
from flask_login import login_required
from flask_login import current_user
from . import bp
from .utils import BitlyHelper
from config import Config
from ..auth.forms import RegistrationForm, LoginForm
from .forms import CreateTableForm

if Config.TEST:
    from ..mock_models import Model as DBHelper
else:
    from ..models import Model as DBHelper

DB = DBHelper()
BH = BitlyHelper()

@bp.route('/')
def home():
    registrationform = RegistrationForm()
    return render_template('home.html', registrationform=registrationform, loginform=LoginForm())

@bp.route('/account')
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html",
                            createtableform=CreateTableForm(), tables=tables)

@bp.route('/dashboard')
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        time_diff = (now - req['time']).seconds
        print()
        req['wait_minutes'] = "{}.{}".format((time_diff//60),
        str(time_diff % 60).zfill(2))
    return render_template('dashboard.html', requests=requests)

@bp.route('/account/createtable', methods=('POST',))
@login_required
def account_createtable():
    form = CreateTableForm(request.form)

    if form.validate():
        tableid = DB.add_table(form.tablenumber.data,
        current_user.get_id())
        new_url = Config.BASE_URL + "newrequest/" + str(tableid)
        new_url = BH.shorten_url(new_url)
        DB.update_table(tableid, new_url)
        return redirect(url_for('main.account'))
    return render_template("account.html", createtableform=form,
    tables=DB.get_tables(current_user.get_id()))


@bp.route('/account/deletetable')
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('main.account'))

@bp.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly"

@bp.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('main.dashboard'))