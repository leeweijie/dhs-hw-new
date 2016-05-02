from protorpc import messages
from protorpc import message_types


class Task(messages.Message):
    extra_title = messages.StringField(1)
    time_added = message_types.DateTimeField(2)

    subject = messages.StringField(3, required=True)
    type = messages.StringField(4, required=True)
    due_date = message_types.DateTimeField(5)

    task_done = messages.BooleanField(6)
    urlid = messages.StringField(7)


class Tasks(messages.Message):
    tasks = messages.MessageField(Task, 1, repeated=True)


class TasksRequest(messages.Message):
    group = messages.StringField(1)
    task_done = messages.BooleanField(2, required=True)

class TaskRequest(messages.Message):
    urlid = messages.StringField(7)
