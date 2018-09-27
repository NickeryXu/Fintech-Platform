from flask import Blueprint, jsonify, session, request
from bson import ObjectId

course = Blueprint('course', __name__)

#一级目录
@course.route('/course', methods=['GET'])
def course_series():
    from models.course import COURSE
    returnObj = {}
    try:
        returnObj['data'] = {}
        returnObj['data']['courses'] = []
        for data in COURSE.objects:
            dataObj = {}
            dataObj['id'] = str(data.id)
            dataObj['teacher'] = data.teacher
            dataObj['series_title'] = data.series_title
            dataObj['course_description'] = data.course_description
            dataObj['course_tag'] = data.course_tag
            returnObj['data']['courses'].append(dataObj)
        returnObj['info'] = {'result': 1, 'info': '获取成功'}
    except Exception as e:
        print('一级目录:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#二级目录
@course.route('/course/<courseId>', methods=['GET'])
def course_list(courseId):
    from models.course import COURSE
    returnObj = {}
    try:
        courseId = ObjectId(courseId)
        courseObj = []
        data_course = COURSE.objects(id=courseId).first()
        for data in data_course.detail.courses:
            dataObj = {}
            dataObj['uid'] = data['uid']
            dataObj['course'] = data['course']
            courseObj.append(dataObj)
        returnObj['data'] = {'courses': courseObj}
        returnObj['info'] = {'result': 1, 'info': '获取成功'}
    except Exception as e:
        print('二级目录:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#课程内容
@course.route('/course/<courseId>/<uid>', methods=['GET'])
def course_detail(courseId, uid):
    from models.course import COURSE
    from models.user import USER
    returnObj = {}
    try:
        dataObj = {}
        courseId = ObjectId(courseId)
        data = COURSE.objects(id=courseId).first()
        courses = data.detail.courses
        for course in courses:
            if course['uid'] == uid:
                dataObj['uid'] = uid
                dataObj['course'] = course['course']
                dataObj['description'] = course['description']
                dataObj['remark'] = course['remark']
                dataObj['datalink'] = course['datalink']
                userObj = {'course': dataObj['course'], 'id': courseId, 'uid': uid}
                USER.objects(id=session['id']).update_one(push__courses=userObj)
        returnObj['data'] = dataObj
        returnObj['info'] = {'result': 1, 'info': '获取成功'}
    except Exception as e:
        print('课程内容:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#我的课程
@course.route('/course/me', methods=['GET'])
def course_me():
    from models.user import USER
    returnObj = {}
    try:
        coursesObj = []
        data_user = USER.objects(id=session['id']).first()
        data_course = data_user['courses']
        for data in data_course:
            mycourse = {}
            mycourse['id'] = str(data['id'])
            mycourse['uid'] = data['uid']
            mycourse['course'] = data['course']
            coursesObj.append(mycourse)
        returnObj['data'] = {'courses': coursesObj}
        returnObj['info'] = {'result': 1, 'info': '获取成功'}
    except Exception as e:
        print('我的课程:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)