import os
from pathlib import Path
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config.from_object("config.Config")
filedir = Path(__file__).parent.parent / (app.config['UPLOAD_FOLDER'])

# To do:
# on app start check that filedir exists and create if does not
# типа такого, только наверное лучше с Path:
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

api = Api(app)

######################################################



import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# methods -- post and put

# curl --upload-file 'test.txt' 127.0.0.1:4000/upl

@app.route("/upl", methods=["PUT", "POST"])
def post_file():
    """Upload a file."""

    # if "/" in filename:
    #     # Return 400 BAD REQUEST
    #     abort(400, "no subdirectories directories allowed")

    print('1', request)
    print('2', request.data)
    print('3', request.files)
    print('4', request.json)
    print('5', request.headers)
    print('6', request.scheme)
    print('8', request.path)
    print('9', request.method)
    print('11', request.content_type)


    with open(os.path.join(filedir, 'diff_curl'), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


# curl -X POST 127.0.0.1:4000/upload -F 'file=@test.txt' -i

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload_csv():
    print('1', request)
    print('2', request.data)
    print('3', request.files)
    print('4', request.json)
    print('5', request.headers)
    print('6', request.scheme)
    # print('7', request.body)
    print('8', request.path)
    print('9', request.method)
    # print('10', request.encoding)
    print('11', request.content_type)
    # print('12', request.content_params)
    # print('13', request.POST)
    # print('14', request.COOKIES)
    # print('15', request.META)
    # print('16', request.resolver_match)


    for k in request.files:
        print(k, request.files[k])

    # print(request.files.iterlists())
    print(request.files.to_dict())
    
    submitted_file = request.files['file']
    if submitted_file and allowed_filename(submitted_file.filename):
        filename = secure_filename(submitted_file.filename)
        directory = os.path.join(app.config['UPLOAD_FOLDER'], '121212')
        if not os.path.exists(directory):
            os.mkdir(directory)

        submitted_file.save(os.path.join(directory, filename))
        out = {
                'status': 'OK',
                'filename': filename,
                'message': f"{filename} saved successful."
                }
        return jsonify(out)



# ну или как раз - ебануть АПИху и раздербанить на 
# отдельные методы, по-честному
@app.route('/putpost', methods=["PUT", "POST"])
def getter():
    if request.method ==  'POST':
        submitted_file = request.files['file']
        if submitted_file and allowed_filename(submitted_file.filename):
            filename = secure_filename(submitted_file.filename)
            directory = os.path.join(app.config['UPLOAD_FOLDER'], '121212')
            if not os.path.exists(directory):
                os.mkdir(directory)

            submitted_file.save(os.path.join(directory, filename))
            out = {
                    'status': 'OK',
                    'filename': filename,
                    'message': f"{filename} saved successful."
                    }
            return jsonify(out)

    elif request.method ==  'PUT':
        with open(os.path.join(filedir, 'diff_curl'), "wb") as fp:
            fp.write(request.data)

            # Return 201 CREATED
            return "", 201