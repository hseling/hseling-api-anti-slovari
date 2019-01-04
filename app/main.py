from flask import Flask, jsonify, request, send_file, redirect, url_for
from logging import getLogger
import os

import boilerplate

from hseling_api_anti_slovari.process import process_data
from hseling_api_anti_slovari.query import query_data


ALLOWED_EXTENSIONS = ['txt']


log = getLogger(__name__)


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=boilerplate.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=boilerplate.CELERY_RESULT_BACKEND
)
celery = boilerplate.make_celery(app)


@celery.task
def process_task(file_ids_list=None):
    files_to_process = boilerplate.list_files(recursive=True,
                                              prefix=boilerplate.UPLOAD_PREFIX)
    if file_ids_list:
        files_to_process = [boilerplate.UPLOAD_PREFIX + file_id
                            for file_id in file_ids_list
                            if (boilerplate.UPLOAD_PREFIX + file_id)
                            in files_to_process]
    data_to_process = {file_id[len(boilerplate.UPLOAD_PREFIX):]:
                       boilerplate.get_file(file_id)
                       for file_id in files_to_process}
    processed_file_ids = list()
    for processed_file_id, contents in process_data(data_to_process):
        processed_file_ids.append(
            boilerplate.add_processed_file(
                processed_file_id,
                contents,
                extension='txt'
            ))
    return processed_file_ids


@app.route('/upload', methods=['GET', 'POST'])
def upload_endpoint():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": boilerplate.ERROR_NO_FILE_PART})
        upload_file = request.files['file']
        if upload_file.filename == '':
            return jsonify({"error": boilerplate.ERROR_NO_SELECTED_FILE})
        if upload_file and boilerplate.allowed_file(
                upload_file.filename,
                allowed_extensions=ALLOWED_EXTENSIONS):
            return jsonify(boilerplate.save_file(upload_file))
    return boilerplate.get_upload_form()


@app.route('/files/<path:file_id>')
def get_file_endpoint(file_id):
    if file_id in boilerplate.list_files(recursive=True):
        return boilerplate.get_file(file_id)
    return jsonify({'error': boilerplate.ERROR_NO_SUCH_FILE})


@app.route("/load_file", methods=['GET', 'POST'])
def load_file_endpoint():
    if request.method == 'POST':
        print('here')
        file_id = request.json['file']
        print(file_id)
        if file_id in boilerplate.list_files(recursive=True):
            # processed_file = boilerplate.get_file(file_id)
            # print(processed_file.__class__)
            # address = os.path.join('/data', 'minio', file_id)
            # f = boilerplate.get_file(file_id)
            return send_file(file_id, mimetype='text/csv',
                             attachment_filename=file_id, as_attachment=True)
        return jsonify({'error': boilerplate.ERROR_NO_SUCH_FILE})
    return jsonify({'error': boilerplate.ERROR_NO_SUCH_FILE})


@app.route('/files')
def list_files_endpoint():
    return jsonify({'file_ids': boilerplate.list_files(recursive=True)})


@app.route('/process')
@app.route("/process/<file_ids>")
def process_endpoint(file_ids=None):
    file_ids_list = file_ids and file_ids.split(",")
    task = process_task.delay(file_ids_list)
    return jsonify({"task_id": str(task)})


# @app.route("/query/<path:file_id>")
# def query_endpoint(file_id):
#     query_type = request.args.get('type')
#     if not query_type:
#         return jsonify({"error": boilerplate.ERROR_NO_QUERY_TYPE_SPECIFIED})
#     processed_file_id = boilerplate.PROCESSED_PREFIX + file_id
#     if processed_file_id in boilerplate.list_files(recursive=True):
#         return jsonify({"result": query_data({
#             processed_file_id: boilerplate.get_file(processed_file_id)
#         }, query_type=query_type)})
#     return jsonify({"error": boilerplate.ERROR_NO_SUCH_FILE})


def safe_check(arr):
    '''проверка полученных параметров на безопасность'''
    checker = set(['dim', 'nonsense', 'vowel_seq', 'stop_seq', 'loan_affix'])
    if len(set(arr) - checker) > 0:
        return False
    return True


@app.route("/query", methods=['GET', 'POST'])
def query_endpoint():
    if request.method == 'POST':
        conn = boilerplate.get_mysql_connection()
        cur = conn.cursor()
        if request.json['base'] == 'all':
            tables = ['main']
        else:
            # проверяем, одна таблица или несколько
            if isinstance(request.json['tables'], str):
                tables = [request.json['tables'],]
            else:
                tables = request.json['tables']
        res = []
        if not safe_check(tables):
            return jsonify({"error": boilerplate.ERROR_NO_SUCH_FILE})
        string = request.json['string']
        for table in tables:
            if 'regexp' in request.json:
                sql = "SELECT word FROM `hse-api-database`.{} WHERE word REGEXP %s".format(table)
                cur.execute(sql, string)
            else:
                string = '%{}%'.format(string)
                sql = "SELECT word FROM `hse-api-database`.{} WHERE word LIKE %(string)s".format(table)
                cur.execute(sql, {'string': string})
            res += cur.fetchall()
        with open('results.csv', 'w') as f:
            f.write('\n'.join([x[0] for x in res]))
        return send_file('results.csv')
    else:
        return jsonify({"error": boilerplate.ERROR_NO_SUCH_FILE})


@app.route("/status/<task_id>")
def status_endpoint(task_id):
    return jsonify(boilerplate.get_task_status(task_id))


@app.route("/test_mysql")
def test_mysql_endpoint():
    conn = boilerplate.get_mysql_connection()
    cur = conn.cursor()
    cur.execute("show tables in `hse-api-database`")
    schema = dict()
    for table_name in cur.fetchall():
        schema.setdefault(table_name[0].decode('utf-8'), [])
    return jsonify({"schema": schema})


@app.route("/upload_mysql")
def upload_mysql_endpoint():
    conn = boilerplate.get_mysql_connection()
    cur = conn.cursor()
    files = boilerplate.list_files(recursive=True)
    for file in files:
        print(file)
        name = file[:-4]
        print(name)
        cur.execute("SELECT table_name from information_schema.tables where \
            table_schema = 'hse-api-database' and table_name = '%s'", name)
        resp = cur.fetchone()
        print(resp)
        if not resp:
            text = boilerplate.get_file(file).decode('utf-8')
            f = [tuple(x.split(',')[1:]) for x in text.split('\n')[1:300]]
            print(f[:5])
            cur.execute("CREATE TABLE `hse-api-database`.{} \
                (word varchar(300), lemma varchar(300), morphs varchar(300), category varchar(100))".format(name))
            for tup in f:
                try:
                    cur.execute("INSERT INTO `hse-api-database`.{}(word,lemma,morphs,category)\
                        VALUES(%s, %s, %s, %s)".format(name), tup)
                except:
                    print(tup)
                    raise
    # conn.commit()
    # conn.close()
    return redirect(url_for('test_mysql_endpoint'))


def get_endpoints(ctx):
    def endpoint(name, description, active=True):
        return {
            "name": name,
            "description": description,
            "active": active
        }

    all_endpoints = [
        endpoint("root", boilerplate.ENDPOINT_ROOT),
        endpoint("scrap", boilerplate.ENDPOINT_SCRAP,
                 not ctx["restricted_mode"]),
        endpoint("upload", boilerplate.ENDPOINT_UPLOAD),
        endpoint("process", boilerplate.ENDPOINT_PROCESS),
        endpoint("query", boilerplate.ENDPOINT_QUERY),
        endpoint("status", boilerplate.ENDPOINT_STATUS)
    ]

    return {ep["name"]: ep for ep in all_endpoints if ep}


@app.route("/")
def main_endpoint():
    ctx = {"restricted_mode": boilerplate.RESTRICTED_MODE}
    return jsonify({"endpoints": get_endpoints(ctx)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)


__all__ = [app, celery]
