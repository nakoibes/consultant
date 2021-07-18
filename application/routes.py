from pprint import pprint

from application.app import app
from flask import render_template, redirect, url_for
from application.forms import SearchForm
from application.service import IPSearcher, ULSearcher


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    return render_template("main.html", form=form, title="Сервис по оценке контрагента", data={"name": "Поиск"})


@app.route("/search/<inn>", methods=["GET", "POST"])
def search(inn):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    if inn.isdigit():
        if len(inn) == 12:
            handler = IPSearcher(inn)
            result = handler.handle()
        else:
            handler = ULSearcher(inn)
            result = handler.handle()
        if result:
            return render_template("result.html", data=result, form=form)
    else:
        return render_template("not_found_inn.html", inn=inn, form=form)
