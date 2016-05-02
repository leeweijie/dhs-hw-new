import models
import datetime
import constants
from google.appengine.ext import ndb


# Get lists of relevant tasks from a group
def get_tasks(group, user, task_done):

    user_info = get_user_info(user)

    if group not in user_info.groups:  # Check if user in the group
        return False

    if user_info.type == constants.STUDENT:
        query = models.Task.query(
            models.Task.subject.IN(user_info.subject_combination),
            ancestor=ndb.Key('group', group))
    else:  # Teacher
        query = models.Task.query(
            ancestor=ndb.Key('group', group))

    query.order(models.Task.time_added)

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
def get_task(urlid, user):
    task = ndb.Key(urlid=urlid).get()

    user_info = get_user_info(user)

    # Check if user in the task's group
    if task.parent()[1] not in user_info.groups:
        return False
    # Check if task is expired. If it is, delete it
    elif check_expired(task):
        return False
    else:
        return task


def delete_task(urlid, user, user_class):
    task = get_task(urlid, user, user_class)
    if task is not False:  # If user is authorised to delete the task
        try:
            task.key.delete()
        except:
            pass  # Prevent crashes from simultaneous deletion


def get_user_info(user):
    info = models.UserInfo.query(
            ancestor=ndb.Key('email', user.email()))[0]
    return info


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
