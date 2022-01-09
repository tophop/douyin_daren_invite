# -*- coding:utf-8 -*-
import datetime
# from flask_wtf.csrf import CSRFProtect
import os
import requests
# import os
from flask import Flask
from flask import *
import re, time
import json
from flask_cors import *
from jinja2 import *
from ads.douyin_daren.mysql_util import MysqlUtil

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app, resources=r'/*')


@app.route('/', methods=["GET"])
def search():
    if request.method == "GET":
        my = MysqlUtil()
        uninvited = sorted(json.loads(my.query_uninvited(my.con)).get('result'), key=lambda x: x.get('create_time'),
                           reverse=True)
        invited = sorted(json.loads(my.query_invited(my.con)).get('result'),
                         key=lambda x: (x.get('create_time'), x.get('invited_time')), reverse=True)
        return render_template('index.html', **locals())


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    # app.jinja_env.auto_reload=True
    app.run(debug=True, host='0.0.0.0', port=8080)
