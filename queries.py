import models
import datetime
from google.appengine.ext import ndb


# Get lists of relevant tasks
def get_tasks(user, user_class, sort_type, task_done,
              subject_combination, reverse=False):
    query = models.Task.query(
        models.Task.subject.IN(subject_combination),
        ndb.OR(not models.Task.is_private, models.Task.user == user),
        ancestor=user_class)

    if reverse:
        query.order(-sort_type)
    else:
        query.order(sort_type)

    tasks = query.fetch()
    to_remove = []
    for task in tasks:
        if check_expired(task):
            to_remove.append(task)
        else:
            done = check_task_done(task, user)
            if task_done != done:
                to_remove.append(task)

    for task in to_remove:
        tasks.remove(task)
    return tasks


# Use this to get or edit task. Checks if user has authorised access to task
def get_task(urlid, user, user_class):
    task = ndb.Key(urlid=urlid).get()
    if task.key.parent()[1] != user_class:  # Check second value of parent key tuple as equal to user's class
        return False
    elif task.is_private and task.user != user:  # Check if task is yours if its private
        return False
    elif check_expired(task):  # Check if task is expired. If it is, delete it
        return False
    else:
        return task


def delete_task(urlid, user, user_class):
    task = get_task(urlid, user, user_class)
    if task is not False:  # If user is authorised to delete the task
        task.key.delete()
        return True
    return False


def get_subject_combination(user):
    subject_combination = models.SubjectCombination.query(
        models.SubjectCombination.user == user).fetch()
    if subject_combination:
        return subject_combination[0]  # gets the only element from the list
    else:
        return False


def get_user_info(user):
    email = user.email()
    user_info = models.UserInfo.query(ancestor=email).fetch()[0]
    if user_info.user_class:
        return {'user_class', user_info.user_class,
                'groups', user_info.groups,
                'subject_combination', user_info.subject_combination}
    else:
        return {'groups', user_info.groups,
                'subject_combination', user_info.subject_combination}


def check_expired(task):
    if task.due_date > datetime.date.today():
        task.key.delete()
        return True
    else:
        return False


def check_task_done(task, user):
    if task.user_status:
        for user_status in task.user_status:
            if user_status.user == user:
                return user_status.task_done

    return False
