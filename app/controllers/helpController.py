from flask import render_template
from app.auth import login_required


@login_required
def help_page():
    return render_template("dashboard/help.html")