from mongoengine import *
from app import app

connect('fintech', host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'], username=app.config['USERNAME'], password=app.config['PASSWORD'], authentication_source='fintech')

class envInfo(EmbeddedDocument):
    envname = StringField()
    envlink = StringField()

class courseInfo(EmbeddedDocument):
    uid = StringField()
    course = StringField()
    description = StringField()
    remark = StringField()
    datalink = StringField()
    env = ListField(EmbeddedDocumentField(envInfo))

class detailInfo(EmbeddedDocument):
    courses = ListField(EmbeddedDocumentField(courseInfo))

class coursesInfo(EmbeddedDocumentField):
    uid = StringField()
    course = StringField()
    description = StringField()
    datalink = StringField()
    content = StringField()
    env = ListField(EmbeddedDocumentField(envInfo))

# class uidInfo(EmbeddedDocument):


class COURSE(Document):
    meta = {"collection": "course"}
    teacher = StringField()
    series_title = StringField()
    course_description = StringField()
    course_tag = StringField()
    detail = EmbeddedDocumentField(detailInfo)
    courses = DictField()