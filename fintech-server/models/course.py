from mongoengine import *
from app import app

connect('fintech', host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])

class courseInfo(EmbeddedDocument):
    uid = StringField()
    course = StringField()
    description = StringField()
    remark = StringField()
    datalink = StringField()

class envInfo(EmbeddedDocument):
    envname = StringField()
    envlink = StringField()

class detailInfo(EmbeddedDocument):
    courses = ListField(EmbeddedDocumentField(courseInfo))
    env = ListField(EmbeddedDocumentField(envInfo))

class COURSE(Document):
    meta = {"collection": "course"}
    teacher = StringField()
    series_title = StringField()
    course_description = StringField()
    course_tag = StringField()
    detail = EmbeddedDocumentField(detailInfo)