import os
import json
import uuid

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
from workers import task_convert_to_mp4, get_job
from info_path_sys import path_to_project

DOWNLOAD_FOLDER = 'new'
UPLOAD_FOLDER = 'src'
ALLOWED_EXTENSIONS = {'flv', 'mp4', 'avi', 'mov'}

app = Flask(__name__, static_url_path='', template_folder='templates')
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(path_to_project, UPLOAD_FOLDER)  # user do upload
app.config['DOWNLOAD_FOLDER'] = os.path.join(path_to_project, DOWNLOAD_FOLDER)  # user do download


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "%s__%s" % (file_id, filename)))
            task = task_convert_to_mp4.apply_async(args=(filename, file_id))
            data = {'taskID': task.id, 'filename': "%s__%s" % (file_id, filename)}
            return redirect(url_for('progress', data=json.dumps(data)))
    return render_template('home.html', data=None)


@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    if filename is not None:
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename)


@app.route('/progress')  # показывает статус задачи
def progress():
    data = request.values.get('data')
    if data is not None:
        data = json.loads(data)
        taskID = data['taskID']
        job = get_job(taskID)
        if job.state == 'PENDING':
            data['task_status'] = 'PENDING'
        elif job.state == 'PROGRESS':
            data['task_status'] = 'PROGRESS'
        elif job.state == 'SUCCESS':
            data['task_status'] = 'SUCCESS'  # появится ссылка на файл, который можно будет скачать
    else:
        return redirect(url_for('home'))
    return render_template('progress.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
