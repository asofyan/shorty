from flask import request, jsonify

def index():
    if request.method == 'POST':
        return post_index()

    return get_index()

def get_index():
    res = { 'version': '0.0.1' }
    return jsonify(res)

def post_index():
    return jsonify('Ok')
