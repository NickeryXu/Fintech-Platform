# 用户模块
## 用户注册
### request
* method：POST
* path：/sign
* 参数：无
```
{
    username: StringField,
    password: StringField,
    mobile: StringField,
    email: StringField,
    remark: StringField,
}
```
### response

无

## 用户登录
* method：POST
* path：/login
* 参数：无
### request
```
{
    username: StringField,
    password: StringField,
}
```
### response

无

## 更改当前用户信息
### request
* method：PUT
* path：/user/change
* 参数：key
* 说明：请求带参数key时为修改密码

没有参数key：
```
{
    username: StringField
    mobile: StringField,
    email: StringField,
    remark: StringField,
}
```
带有参数key：
```
{
    password: StringField,
}
```
### response

无

## 用户登出
### request
* method：GET
* path：/users/logout
* 参数：无
### response

无

# 课程模块
## 一级目录
### request
* method：GET
* path：/course
* 参数：无
### response
```
{
    data:{
        courses:[{
            _id: StringField,
            teacher: StringField,
            series_title: StringField,
            course_description: STringFIeld,
            course_tag: StringField
        }]
    },
    info:{
        info: StringField,
        result: IntField,
    }
}
```
## 二级目录
* method：GET
* path：/course/:courseId
* 说明：corseId为一级目录的id
### request

无

### response
```
{
    data:{
        courses:[
            {
                uid: StringField,
                course: StringField
            },
        ]
    },
    info:{
        info: StringFIeld,
        result: IntField,
    }
}
```
## 课程内容
### request
* method：GET
* path：/course/:courseId/:uid
* 说明：uid为二级目录的id
### response
```
{
    data:{
        uid: StringField,
        course: StringFIeld,
        description: StringField,
        remark: StringField,
        datalink: StringField,
    },
    info:{
        info: StringFIeld,
        result: IntField,
    }
}
```
## 我的课程
### request
* method：GET
* path：/course/me
* 参数：无
### response
```
{
    data:{
        courses:[
            {
                id: StringField,
                uid: StringField
                course: StringField,
            }
        ]
    },
    info:{
        info: StringFIeld,
        result: IntField,
    }
}
```
## 提交作业
### request
* method：POST
* path：/course/:courseId/:uid
```
{
    id: StringField,
    uid: StringField,
    course: StringField,
    content: StringField,
}
```
### response
无