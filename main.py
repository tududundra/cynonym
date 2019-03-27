from flask import Flask, flash, redirect, render_template, request, session, abort, current_app
from flask_pager import Pager
import os
import json
from database import find_line, get_words

word_list = get_words()

with open("/home/Cynonym/mysite/tests.json", "r") as read_file:
    tests_data = json.load(read_file)

app = Flask(__name__)

app.secret_key = os.urandom(42)
app.config['PAGE_SIZE'] = 15
app.config['VISIBLE_PAGE_COUNT'] = 20


@app.route("/")
def index():
    page = int(request.args.get('page', 1))
    count = len(word_list)
    data = sorted(word_list)
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[skip: skip + limit]
    return render_template('slovar.html', pages=pages, data_to_show=data_to_show)


@app.route('/search', methods=['POST', 'GET'])
def search():

    page = int(request.args.get('page', 1))
    count = len(word_list)
    data = sorted(word_list)
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = data[skip: skip + limit]

    if request.method == 'POST':
        result = request.form
        response = find_line(result['Word'].lower())
        if response is not None:
            test_data = tests_data[str(response['id'])]
            return render_template('result.html', response=response, word=result['Word'], test_data=test_data)
        else:
            return render_template('slovar.html', pages=pages, data_to_show=data_to_show, error=True)


@app.route('/selected/<string:word>', methods=['GET', 'POST'])
def selected(word):
    response = find_line(word)
    if response is not None:
        test_data = tests_data[str(response['id'])]
        return render_template('result.html', response=response, word=word, test_data=test_data)


@app.route("/Info")
def info():
    return render_template('info.html')


@app.route("/Instruction")
def instruction():
    return render_template('instruction.html')

if __name__ == "__main__":
    app.run()
