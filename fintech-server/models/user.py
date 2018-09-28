from mongoengine import *
from app import app

connect('fintech', host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])

class courseInfo(EmbeddedDocument):
    id = ObjectIdField()
    uid = StringField()
    course = StringField()

class feedbackInfo(EmbeddedDocument):
    id = ObjectIdField()
    uid = StringField()
    course = StringField()
    content = StringField()
    RecordTime = StringField()

class USER(Document):
    meta = {'collection': 'user'}
    username = StringField(required=True, unique=True)
    password = StringField()
    email = StringField()
    mobile = StringField()
    remark = StringField()
    LastloginTime = StringField()
    courses = ListField(EmbeddedDocumentField(courseInfo))
    feedbacks = ListField(EmbeddedDocumentField(feedbackInfo))

