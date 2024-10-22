from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Account, Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/history/<int:account_id>')
@login_required
def transaction_history(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        abort(403)
    
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return render_template('transaction_history.html', transactions=transactions, account=account)
