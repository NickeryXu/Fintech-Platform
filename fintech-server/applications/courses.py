from flask import Blueprint, jsonify, session, request, render_template
from bson import ObjectId
from auth import sign_check

course = Blueprint('course', __name__)

#一级目录
@sign_check()
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
        return render_template('course.html', courses=returnObj['data']['courses'])

# #二级目录
# @sign_check()
# @course.route('/course/<courseId>', methods=['GET'])
# def course_list(courseId):
#     from models.course import COURSE
#     returnObj = {}
#     try:
#         courseId = ObjectId(courseId)
#         courseObj = []
#         data_course = COURSE.objects(id=courseId).first()
#         for data in data_course.detail.courses:
#             dataObj = {}
#             dataObj['uid'] = data['uid']
#             dataObj['course'] = data['course']
#             courseObj.append(dataObj)
#         returnObj['data'] = {'courses': courseObj}
#         returnObj['info'] = {'result': 1, 'info': '获取成功'}
#     except Exception as e:
#         print('二级目录:', e)
#         returnObj['data'] = {}
#         returnObj['info'] = {'result': 500, 'info': '后台异常'}
#     finally:
#         return render_template('learn.html', courses=returnObj['data']['courses'])
#
# #课程内容
# @sign_check()
# @course.route('/course/<courseId>/<uid>', methods=['GET'])
# def course_detail(courseId, uid):
#     from models.course import COURSE
#     from models.user import USER
#     returnObj = {}
#     try:
#         dataObj = {}
#         courseId = ObjectId(courseId)
#         data = COURSE.objects(id=courseId).first()
#         courses = data.detail.courses
#         for course in courses:
#             if course['uid'] == uid:
#                 dataObj['uid'] = uid
#                 dataObj['course'] = course['course']
#                 dataObj['description'] = course['description']
#                 dataObj['remark'] = course['remark']
#                 dataObj['datalink'] = course['datalink']
#                 userObj = {'course': dataObj['course'], 'id': courseId, 'uid': uid}
#                 data_user = USER.objects(id=ObjectId(session['id'])).first()
#                 data_courses = data_user.courses
#                 i = 0
#                 for n in data_courses:
#                     if n['id'] == courseId:
#                         n['uid'] = uid
#                         n['course'] = course['course']
#                         data_user.save()
#                         i = 1
#                 if i != 1:
#                     USER.objects(id=ObjectId(session['id'])).update_one(push__courses=userObj)
#         returnObj['data'] = dataObj
#         returnObj['info'] = {'result': 1, 'info': '获取成功'}
#     except Exception as e:
#         print('课程内容:', e)
#         returnObj['data'] = {}
#         returnObj['info'] = {'result': 500, 'info': '后台异常'}
#     finally:
#         return jsonify(returnObj)

#我的课程
@sign_check()
@course.route('/course/me', methods=['GET'])
def course_me():
    from models.user import USER
    returnObj = {}
    try:
        coursesObj = []
        data_user = USER.objects(id=ObjectId(session['id'])).first()
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

#提交作业
@sign_check()
@course.route('/course/<courseId>/<uid>', methods=['POST'])
def homework_put(courseId, uid):
    from models.user import USER
    import time
    returnObj = {}
    try:
        feedbackObj = {}
        id = courseId
        uid = uid
        course = request.json.get('course')
        content = request.json.get('content')
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        feedbackObj['id'] = id
        feedbackObj['uid'] = uid
        feedbackObj['course'] = course
        feedbackObj['content'] = content
        feedbackObj['RecordTime'] = time_now
        USER.objects(id=ObjectId(session['id'])).update_one(push__feedbacks=feedbackObj)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 1, 'info': '提交成功'}
    except Exception as e:
        print('我的课程:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return jsonify(returnObj)

#课程内容
@sign_check()
@course.route('/course/<courseId>', methods=['GET'])
def course_detail(courseId):
    import hashlib
    import json
    # from websocket import create_connection
    import urllib
    from models.course import COURSE
    from models.user import USER
    returnObj = {}
    try:
        courseId = ObjectId(courseId)
        data_course = COURSE.objects(id=courseId).first()
        courseArray = []
        courses_detail = data_course.courses
        for key, value in courses_detail.items():
            dataObj = {}
            dataObj['courseId'] = str(courseId)
            dataObj['uid'] = key
            dataObj['course'] = value['course']
            courseArray.append(dataObj)
        # 查询课程历史记录
        # data_user = USER.objects(id=session['id']).first()
        # n = 0
        # courses = data_user.courses
        # for course in courses:
        #     if course['id'] == courseId:
        #         n = course['uid']
        # if n == 0:
        #     uid = 1
        # else:
        #     uid = n
        returnObj['courses'] = courseArray
        uid = request.args.get('uid')
        # print(uid)
        if not uid:
            returnObj['course'] = {}
        else:
            courseObj = {}
            course = courses_detail[uid]
            courseObj['courseId'] = str(courseId)
            courseObj['uid'] = uid
            courseObj['course'] = course['course']
            courseObj['description'] = course['description']
            # courseObj['remark'] = course['remark']
            courseObj['datalink'] = course['datalink']
            courseObj['content'] = course['content']
            courseObj['env'] = course['env']
            # userObj = {'course': courseObj['course'], 'id': courseId, 'uid': uid}
            # data_user = USER.objects(id=ObjectId(session['id'])).first()
            # data_courses = data_user.courses
            # i = 0
            # for n in data_courses:
            #     if n['id'] == courseId:
            #         n['uid'] = uid
            #         n['course'] = course['course']
            #         data_user.save()
            #         i = 1
            # if i != 1:
            #     USER.objects(id=ObjectId(session['id'])).update_one(push__courses=userObj)
            returnObj['course'] = courseObj
            # print('course =', courseObj)
        envname = request.args.get('envname')
        returnObj['env'] = {}
        if envname:
            sha = hashlib.sha1()
            userid = session.get('id')
            sha.update(userid.encode('utf-8'))
            sha.update(str(courseId).encode('utf-8'))
            Oid = sha.hexdigest()[0:16]
            # ws = create_connection('http://api.datadynamic.io/api/v1/instance/' + ownerid + '/eureka')
            # result = ws.recv()
            # http://api.datadynamic.io/api/v1/instance/aacc1122344deerr/eureka
            url = 'http://api.datadynamic.io/api/v1/instance/' + Oid + '/eureka'
            req = urllib.request.Request(url=url, data={})
            res = urllib.request.urlopen(req)
            res = json.loads(res.read())[0]
            Cid = res['id'][0:16]
            link = 'http://' + Cid + '-8888-env1.env.datadynamic.io/notebooks/Welcome.ipynb'
            envObj = {Oid: link}
            USER.objects(id=ObjectId(session['id'])).update_one(push__envlink=envObj)
            # for env in course['env']:
            #     if env['envname'] == envname:
            #         env['envlink'] = link
            #         returnObj['env'] = {'envname': envname, 'envlink': env['envlink']}
            returnObj['env'] = {'envname': envname, 'envlink': link}
            print(link)
    except Exception as e:
        print('课程内容:', e)
        returnObj['data'] = {}
        returnObj['info'] = {'result': 500, 'info': '后台异常'}
    finally:
        return render_template('learn.html', courses=returnObj['courses'], course=returnObj['course'], env=returnObj['env'])

