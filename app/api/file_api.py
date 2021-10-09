import os
from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from app.common.response import ResMsg
from app.utils.code import ResponseCode

bp = Blueprint("test", __name__, url_prefix='/')


@bp.route('/uploader', methods=['POST'])
def uploader():
    res = ResMsg()
    f = request.files['file']
    f.save(os.path.join('C:\\Users\\Administrator\\Desktop\\', secure_filename(f.filename)))
    res.update(code=ResponseCode.Success,data='上传成功')
    return jsonify(res.data)


@bp.route("/unifiedResponse", methods=["GET"])
def test_unified_response():
    """
    测试统一返回消息
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)
