from flask import render_template


def about():
    return render_template("pages/about.html")


def contact():
    return render_template("pages/contact.html")


def terms():
    return render_template("pages/terms.html")


def privacy():
    return render_template("pages/privacy.html")