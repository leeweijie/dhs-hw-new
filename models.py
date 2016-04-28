import constants
from google.appengine.ext import ndb


class Task(ndb.Model):  # Class is the ancestor
    name = ndb.StringProperty(required=True)
    user = ndb.UserProperty(auto_current_user_add=True, indexed=True, required=True)
    time_added = ndb.DateTimeProperty(auto_now_add=True, required=True)

    subject = ndb.StringProperty(choices=constants.ALL_SUBJECTS, required=True)
    is_private = ndb.BooleanProperty(default=False, required=True)
    due_date = ndb.DateProperty()
    time_needed = ndb.IntegerProperty(choices=constants.TIME_NEEDED_RANGE)
    priority = ndb.IntegerProperty(choices=constants.PRIORITY_RANGE)

    user_status = ndb.StructuredProperty(UserStatus, repeated=True)


class UserStatus(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add=True, indexed=True, required=True)
    task_done = ndb.BooleanProperty(required=True)


class SubjectCombination(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add=True, indexed=True, required=True)
    subject_combination = ndb.StringProperty(choices=constants.ALL_SUBJECTS, repeated=True)


class UserInfo(ndb.Model):  # Ancestor is user's email. Form: ('email', email)
    type = ndb.IntegerProperty(constants.USER_TYPE.items(), required=True)
    user_class = ndb.StringProperty()  # If user is  student
    groups = ndb.StringProperty(repeated=True)
    subject_combination = ndb.StructuredProperty(SubjectCombination)
