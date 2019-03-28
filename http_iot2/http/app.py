# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
import time
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
TIME = ['-'] * 7
TEMP = ['-'] * 7

def output(msg):
    TEMP.pop(0)
    TEMP.append(str(msg).split()[-1].strip())
    TIME.pop(0)
    TIME.append(str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
    with open('out_http.txt','a',encoding='utf-8') as f:
        f.write(msg+'\n')

def read_data(path):
    lines = [] 
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) <7:
        return lines
    else:
        lines = list(map(str.strip,lines[-7:]))
        ans = ''
        for i in range(len(lines)):
            ans += '<td>'
            temp = str(lines[i]).split()[-1].strip()
            ans+= temp
            ans+='</td>'
        return ans

# get name value from query string and cookie
@app.route('/iot')
def iot():
    name = request.args.get('name')
    output(str(name))
    print(name)
    response = '<h1>data is %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    return response

@app.route('/show')
def show():
    # print(TEMP)
    response = '<table border="1">'
    ti = '<td> Time </td>'
    for i in range(len(TIME)):
        ti += '<td>{}</td>'.format(str(TIME[i]))
        # ti += '&nbsp &nbsp &nbsp'

    temp = '<td> 超声波 </td>'

    for i in range(len(TEMP)):
        temp += '<td>{}</td>'.format(str(TEMP[i]))
        # temp += '&nbsp &nbsp &nbsp'

    response += '<tr>{}</tr>'.format(ti)
    response += '<tr>{}</tr>'.format(temp)  # escape name to avoid XSS
    response += '<tr> <td> Rotation mqtt </td>{}</tr>'.format(read_data('../../mqtt/out_mqtt.txt'))
    response += '<tr> <td> Light coap </td>{}</tr>'.format(read_data('../../out_coap.txt'))
    response += '<tr> <td> Temprature socket </td>{}</tr>'.format(read_data('../../socket/out_socket.txt'))
    # return different response according to the user's authentication status
    response += '</table>'
    return response

# get name value from query string and cookie
@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# redirect
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# use int URL converter
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2018 - year)


# use any URL converter
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    abort(404)



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
