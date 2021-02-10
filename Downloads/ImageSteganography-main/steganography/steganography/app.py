from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from algo import Steganography
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/validate', methods=['POST', 'GET'])
def validate():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('/encrypt')
        else:
            return render_template('index.html')
    return redirect('/')


@app.route('/encrypt')
def encrypt():
    return render_template('encrypt.html')


@app.route('/encrypt_validate', methods=['POST', 'GET'])
def encrypt_validate():
    if request.method == 'POST':
        message = request.form.get('message')
        email = request.form.get('email')
        target = os.path.join(APP_ROOT, 'utils')
        file_name = ''
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "\\".join([target, filename])
            file_name = destination
            print(destination)
            file.save(destination)
        Steganography.encode(file_name, message, email)
        return redirect('/encrypt')
    else:
        return redirect('/encrypt')


@app.route('/decode')
def decode():
    return render_template('dec.html')


@app.route('/dec_validate', methods=['POST', 'GET'])
def dec():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static\\image')
        file_name = ''
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "\\".join([target, filename])
            file_name = destination
            file.save(destination)
        msg = Steganography.decode(file_name)
        print(msg)
        return render_template('dec.html', msg=msg)
    else:
        return redirect('/encrypt')


if __name__ == '__main__':
    app.run(debug=True)
