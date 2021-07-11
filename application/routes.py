from application.app import app
from flask import render_template, flash, redirect, url_for
from application.forms import SearchForm
import requests


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    return render_template("main.html", form=form)


@app.route("/search/<inn>", methods=["GET", "POST"])
def search(inn):
    key = "6b6d3dc1db81eb304b998af41ef6e91d47b3bb5f"
    r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={key}", )
    if r.json():
        return r.json().get("items")[0].get("ЮЛ").get("Адрес").get("АдресПолн")
    return "Неверный инн"
