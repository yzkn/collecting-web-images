# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Markup
from icrawler.builtin import GoogleImageCrawler
import hashlib
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def test():
    term = ''
    try:
        if request.method == 'POST':
            term = request.form['term']
        else:
            term = request.args.get('term', '')

        if term == '':
            return render_template('index.html')
        else:
            return render_template('index.html', term=term)
    except Exception as e:
        return str(e)


@app.route('/search/<term>')
def hello(term=''):
    if term == '':
        return render_template('index.html')
    else:
        return render_template('index.html', term=term)

def collect(term=''):
    if term != '':
        hs = hashlib.sha256(term.encode()).hexdigest()
        crawler = GoogleImageCrawler(storage={'root_dir': hs})
        crawler.crawl(keyword=term, max_num=100)

        # zip

        # Download
        response = make_response()
        filename = hs + '.zip'
        response.data = open(filename, 'rb').read()
        downloadFileName = 'download.zip'
        response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName

        # ★ポイント4
        response.mimetype = XLSX_MIMETYPE
        return response

if __name__ == '__main__':
    app.run()