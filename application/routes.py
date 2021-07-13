from pprint import pprint

from application.app import app
from flask import render_template, redirect, url_for
from application.forms import SearchForm
from application.service import IPSearcher, ULSearcher
from application.app import session


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    return render_template("main.html", form=form)


@app.route("/search/<inn>", methods=["GET", "POST"])
def search(inn):
    inn = inn
    if len(inn) == 12:
        handler = IPSearcher(inn)
        result = handler.handle()
    else:
        handler = ULSearcher(inn, session)
        result = handler.handle()
    # pprint(result)
    if result:
        return render_template("result.html", data=result)
    else:
        return "Неверный ИНН"
