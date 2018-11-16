from flask import session, jsonify, redirect
from functools import wraps
from models.user import USER
import time

def sign_check():
    def sign_decorator(f):
        @wraps(f)
        def sign_function(*args, **kwargs):
            try:
                returnObj = {}
                if 'username' not in session:
                    returnObj['data'] = {}
                    returnObj['info'] = {"result": "400", "info": "请登录后进行操作"}
                    return redirect('/login')
                print('check session success!')
            except Exception as e:
                print("sign_check's error:", e)
                returnObj['data'] = {}
                returnObj['info'] = {"result": "500", "info": "check后台异常"}
                return jsonify(returnObj)
            finally:
                pass
            return f(*args, **kwargs)
        return sign_function
    return sign_decorator

def Oid_check():
    def Oid_decorator(f):
        @wraps(f)
        def Oid_function(*args, **kwargs):
            try:
                data = USER.objects(id=session['id']).first()
                envlink = data.envlink
                for Oid, env in envlink.items():
                    time_now = time.strftime('%Y-%m-%d %X', time.gmtime())
                    if env[1] < time_now:
                        print('Oid clear!', Oid)
                        del envlink[Oid]
                        continue
                USER.objects(id=session['id']).update_one(envlink=envlink)
            except Exception as e:
                print("Oid_check's error:", e)
            finally:
                pass
            return f(*args, **kwargs)
        return Oid_function
    return Oid_decorator

