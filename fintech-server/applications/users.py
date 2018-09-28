from flask import Blueprint, jsonify, session, request
from bson import ObjectId
from auth import sign_check

user = Blueprint('user', __name__)

#登录
@user.route('/login', methods=['POST'])
def user_login():
    from models.user import USER
    import time
    returnObj = {}
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        data_user = USER.objects(username=username, password=password).first()
        if data_user:
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            USER.objects(username=username).update(LastloginTime=time_now)
            session['id'] = str(data_user.id)
            session['username'] = data_user.username
            returnObj['data'] = {}
            returnObj['info'] = {'result': 1, 'info': '登陆成功'}
        else:
            returnObj['data'] = {}
            returnObj['info'] = {'result': 400, 'info': '登录失败'}
    except Exception as e:
        print('user_login:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#获取当前用户
@sign_check()
@user.route('/users/me', methods=['GET'])
def user_me():
    from models.user import USER
    returnObj = {}
    try:
        data = {}
        username = session['username']
        data_user = USER.objects(username=username).first()
        data['_id'] = session['id']
        data['username'] = username
        data['email'] = data_user.email
        data['remark'] = data_user.remark
        data['LastloginTime'] = data_user.LastloginTime
        data['mobile'] = data_user.mobile
        returnObj['data'] = data
        returnObj['info'] = {'result': 1, 'info': '返回成功'}
    except Exception as e:
        print('user_me:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#注册
@user.route('/sign', methods=['POST'])
def create_user():
    from models.user import USER
    returnObj = {}
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        mobile = request.json.get('mobile')
        remark = request.json.get('remark')
        courses = []
        feedbacks = []
        data = USER.objects(username=username).first()
        if not password:
            returnObj['data'] = {}
            returnObj['info'] = {'result': 400, 'info': '请输入密码'}
        elif data:
            returnObj['data'] = {}
            returnObj['info'] = {'result': 400, 'info': '用户名重复'}
        else:
            sign = USER(
                username=username,
                password=password,
                mobile=mobile,
                email=email,
                remark=remark,
                courses=courses,
                feedbacks=feedbacks
            )
            sign.save()
            returnObj['data'] = {}
            returnObj['info'] = {'result': 1, 'info': '创建成功'}
    except Exception as e:
        print('create_user:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#更改当前用户
@sign_check()
@user.route('/users/change', methods=['PUT'])
def change_one():
    from models.user import USER
    returnObj = {}
    try:
        id = session.get('id')
        username = request.json.get('username')
        password = request.json.get('password')
        mobile = request.json.get('mobile')
        email = request.json.get('email')
        remark = request.json.get('remark')
        USER.objects(id=ObjectId(id)).update(username=username, password=password,\
                                       mobile=mobile, email=email, remark=remark)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 1, 'info': '更改成功'}
    except Exception as e:
        print('change_one:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#用户登出
@user.route('/users/logout', methods=['GET'])
def logout():
    returnObj = {}
    returnObj['data'] = {}
    returnObj['info'] = {'result': 1, 'info': '登出成功'}
    return jsonify(returnObj)