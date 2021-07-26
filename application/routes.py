import json
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup
from ast import literal_eval
import pdfkit as pdf
import requests as requests

from application.app import app, db
from flask import render_template, redirect, url_for, request, Response, jsonify
from application.forms import SearchForm
from application.service import ULSearcher, analyze


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    return render_template("main.html", form=form, title="Сервис по оценке контрагента", data={"name": "Поиск"})


@app.route("/search/<inn>", methods=["GET", "POST"])
def search(inn):
    form = SearchForm()
    # if otchet_form.validate_on_submit():
    #     otchet(result)
    if form.validate_on_submit():
        return redirect(url_for("search", inn=form.search_field.data))
    if inn.isdigit():
        if not get_from_db(inn):
            if len(inn) == 10:
                handler = ULSearcher(inn)
                result = handler.handle()
                db.get_collection("consultant").insert_one(result)
            else:
                result = None
        else:
            result = get_from_db(inn)
        if result:
            result.update({"date": datetime.today().strftime("%-d %B %Y")})

            warn = analyze(result)
            result = alter(result)
            if result.get("nalog_debt") == "Не имеет задолженность":
                result.update({"nalog_debt": "Задолженностей не выявлено"})
            print(result)
            return render_template("result.html", data=result, form=form, warn=warn)
        else:
            return render_template("not_found_inn.html", inn=inn, form=form, data={})
    else:
        return render_template("not_found_inn.html", inn=inn, form=form, data={})


@app.route("/otchet")
def otchet():
    data = request.args.get("data")
    data = literal_eval(data)
    options = {'enable-local-file-access': None, 'encoding': "UTF-8"}
    res = pdf.from_string(render_template("otchet.html", data=data, warn={}), False,
                          css="application/static/otchet.css", options=options)
    response = Response(res, mimetype="application/pdf")
    response.headers['Content-Disposition'] = "attachment; filename=result.pdf"

    return response


def get_from_db(inn):
    ans = db.get_collection("consultant").find_one({"inn": inn})
    if ans:
        ans.pop("_id", None)
    return ans


def alter(result):
    if result.get("status") == "Прекратило деятельность":
        result.pop("time_delta", None)
    return result
