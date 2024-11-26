from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
# Create a blueprint for the main routes
main_bp = Blueprint('main', __name__)

# Home route to render the base.html template
@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('accounts.dashboard'))
    return render_template('base.html')
