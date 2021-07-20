from pprint import pprint

from application.app import app, db
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
        if not get_from_db(inn):
            if len(inn) == 12:
                handler = IPSearcher(inn)
                result = handler.handle()
            else:
                handler = ULSearcher(inn)
                result = handler.handle()
            db.get_collection("consultant").insert_one(result)
        else:
            result = get_from_db(inn)
        if result:
            #print(result)
            return render_template("result.html", data=result, form=form)
    else:
        return render_template("not_found_inn.html", inn=inn, form=form,data = {})


def get_from_db(inn):
    return db.get_collection("consultant").find_one({"inn": inn})
