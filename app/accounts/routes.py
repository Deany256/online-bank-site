from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Account
from app.accounts.forms import AccountForm
from app import db

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/dashboard')
@login_required
def dashboard():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', accounts=accounts)

@accounts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_account():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(
            account_type=form.account_type.data,
            balance=form.initial_deposit.data,
            user_id=current_user.id
        )
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('accounts.dashboard'))
    return render_template('create_account.html', form=form)


@accounts_bp.route('/account/<int:account_id>')
@login_required
def account_details(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        abort(403)
    return render_template('account_details.html', account=account)
