from flask import Blueprint
from . import index

mod = Blueprint('api', __name__)


@mod.route('/', methods=['GET', 'POST'])
def home():
    return index.index()



# @mod.route('/url/<code>', methods=['GET'])
# def get_url(code):
#     print('code', code)
#     return url.get_url(code)
