from flask import render_template
from . import main

# 这个为什么路由是'/' 呢， 因为在地址栏看网址是127:0.0.1:5000但是你复制粘贴出来是http://127.0.0.1:5000/,
# 因为浏览器把他给省略了
@main.route('/')
def index():
    return render_template('index.html')
