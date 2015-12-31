#coding:utf-8
from flask import Flask, url_for, redirect, flash, jsonify
from flask import request, make_response
from urllib import urlencode
from flask import render_template
from . import main
from models import db, Post_account, User
from datetime import datetime, date, time
from werkzeug import secure_filename
import string
import uuid
import requests
import simplejson
import hashlib
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


UPLOAD_FOLDER = "./app/static/images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def gen_file_name(filepath, filename):
    filepath = filepath + '/' + filename[0:6]
    # while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
    # filename = '%s_%s%s' % (name, str(i), extension)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    return filepath


@main.route('/')
def index():
    return render_template('index.html')

@main.route("/post_account_list")
def post_account_list():
    accounts = Post_account.query.all()
    return render_template('post_account_list.html', accounts=accounts)

@main.route("/add_account")
def add_account():
    return render_template('add_account.html')

@main.route("/add_account_info", methods=['POST'])
def add_account_info():
    website = request.form["website"]
    account = request.form["account"]
    password = request.form["password"]
    account_info = Post_account(account=account, website=website, password=password)
    db.session.add(account_info)
    db.session.commit()
    if account_info.id is not None:
        return redirect("/post_account_list")
    else:
        return "error"
        # return render_template('add_account.html')

@main.route("/edit_account")
def edit_account():
    id = request.args.get('id')
    account = Post_account.query.filter_by(id=id).first()
    return render_template('edit_account.html', account=account)


@main.route("/edit_account_info", methods=['POST'])
def edit_account_info():
    id = request.form["id"]
    account = Post_account.query.filter_by(id=id).first()
    account.website = request.form["website"]
    account.account = request.form["account"]
    account.password = request.form["password"]
    db.session.add(account)
    db.session.commit()
    return redirect("/post_account_list")


@main.route("/delete_account")
def delete_account():
    id = request.args.get("id")
    print id,"__________+_+_+"
    account = Post_account.query.filter_by(id=id).first()
    db.session.delete(account)
    db.session.commit()
    return redirect("/post_account_list")

@main.route("/add_user")
def add_user():
    return render_template('add_user.html')


@main.route("/add_user_info", methods=['POST'])
def add_user_info():
    head_image = None
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid1()) + '.' + filename.rsplit('.', 1)[1].lower()
        filepath = gen_file_name(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file_path = os.path.join(filepath, filename)
        file.save(uploaded_file_path)
        head_image = uploaded_file_path[5:]

    name = request.form["name"]
    phone = request.form["phone"]
    times = datetime.now()
    user_info = User(name=name, phone=phone, head_image=head_image, created_times=times)
    db.session.add(user_info)
    db.session.commit()
    if user_info.id is not None:
        return redirect("/user_list")
    else:
        return "error"


@main.route("/edit_user")
def edit_user():
    id = request.args.get('id')
    user_info = User.query.filter_by(id=id).first()
    return render_template('edit_user.html', user=user_info)


@main.route("/edit_user_info", methods=['POST'])
def edit_user_info():
    head_image = None
    if request.files['file'] is not None :
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid1()) + '.' + filename.rsplit('.', 1)[1].lower()
            filepath = gen_file_name(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file_path = os.path.join(filepath, filename)
            file.save(uploaded_file_path)
            head_image = uploaded_file_path[5:]

        id = request.form["id"]
        user = User.query.filter_by(id=id).first()
        user.name = request.form["name"]
        user.phone = request.form["phone"]
        if head_image is not None:
            user.head_image = head_image
        db.session.add(user)
        db.session.commit()
        return redirect("/user_list")


@main.route("/user_list")
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@main.route("/delete_user")
def delete_user():
    id = request.args.get("id")
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/user_list")