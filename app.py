# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, make_response, Markup, render_template, request
from icrawler.builtin import GoogleImageCrawler
import hashlib
import os
import shutil


datadir = 'data'
maximg = 200


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
            return collect(term)
    except Exception as e:
        # return str(e)
        pass


@app.route('/search/<term>')
def hello(term=''):
    try:
        if term == '':
            return render_template('index.html')
        else:
            return collect(term)
    except Exception as e:
        # return str(e)
        pass

def collect(term=''):
    if os.path.exists(datadir):
        shutil.rmtree(datadir)
    os.makedirs(datadir)

    if term != '':
        print('term: '+ term)
        hs = hashlib.sha256(term.encode()).hexdigest()
        dtstr = datetime.now().strftime('%Y%m%d%H%M%S')

        imgdir  = datadir + os.path.sep + hs # dir
        print('imgdir: '+ imgdir)
        basename = datadir + os.path.sep + ( hs + '_' + dtstr ) # filename - ext
        print('basename: '+ basename)
        filename = basename + '.zip' # filename
        print('filename: '+ filename)
        downloadfilename = dtstr + '.zip' # header
        print('downloadfilename: '+ downloadfilename)

        # Collect
        crawler = GoogleImageCrawler(storage={'root_dir': imgdir})
        print('GoogleImageCrawler')
        crawler.crawl(keyword=term, max_num=maximg)
        print('crawler: ' + term + ' : ' + str(maximg))

        # zip
        shutil.make_archive(basename, 'zip', root_dir=imgdir)
        print('make_archive')

        shutil.rmtree(imgdir)
        print('rmtree')

        # Download
        response = make_response()
        print('make_response')
        response.data = open(filename, 'rb').read()
        print('open')
        response.headers['Content-Disposition'] = 'attachment; filename=' + downloadfilename
        print('Content-Disposition')
        response.mimetype = 'application/zip'
        print('mimetype')
        return response

if __name__ == '__main__':
    app.run()