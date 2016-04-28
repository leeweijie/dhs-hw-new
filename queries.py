import models
import datetime
from google.appengine.ext import ndb


def get_tasks(user, user_class, sort_type, task_done, reverse=False):
    query = models.Task.query(
        ndb.OR(not models.Task.is_private, models.Task.user == user),
        ancestor=user_class)
    if reverse:
        query.order(-sort_type)
    else:
        query.order(sort_type)

    tasks = query.fetch()
    to_remove = []
    for task in tasks:
        if task.due_date
            and task.due_date>datetime.
        if task.user_status:
            for user_status in task.user_status:
                if user_status.user == user:
                    task.task_done = user_status.task_done

def check_expired(task):
    if task.due_date > datetime.date.today():
        task.key.delete()
        return True
    else:
        return False
