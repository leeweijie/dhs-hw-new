import constants
from google.appengine.ext import ndb


class Task(ndb.Model):  # Class is the ancestor
    extra_title = ndb.StringProperty()
    user = ndb.UserProperty(indexed=True, required=True)
    time_added = ndb.DateTimeProperty(auto_now_add=True, required=True)
    type = ndb.StringProperty(choices=constants.TASK_TYPE, required=True)
    subject = ndb.StringProperty(choices=constants.ALL_SUBJECTS, required=True)
    due_date = ndb.DateProperty()


class UserStatus(ndb.Model):  # Ancestor is the task key
    user = ndb.UserProperty(indexed=True, required=True)
    task_done = ndb.BooleanProperty(required=True)


class SubjectCombination(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add=True, indexed=True, required=True)
    subject_combination = ndb.StringProperty(choices=constants.ALL_SUBJECTS, repeated=True)


# User info added by admin
class UserInfo(ndb.Model):  # Ancestor is user's email. Form: ('email', email)
    type = ndb.IntegerProperty(constants.USER_TYPE, required=True)  # Whether user is a student or teacher
    groups = ndb.StringProperty(repeated=True)
    subject_combination = ndb.StructuredProperty(SubjectCombination)
