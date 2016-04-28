from protorpc import messages
from protorpc import message_types


class Task(messages.Message):
    name = messages.StringField(1, required=True)
    time_added = message_types.DateTimeField(2)

    subject = messages.StringField(3, required=True)
    is_private = messages.BooleanField(4, default=False, required=True)
    due_date = message_types.DateTimeField(5)
    time_needed = messages.IntegerField(6)
    priority = messages.IntegerField(7)

    task_done = messages.BooleanField(8, required=True)


class SubjectCombination(messages.Message):
    subject_combination = messages.StringField(1, repeated=True)


class Tasks(messages.Message):
    tasks = messages.MessageField(Task, 1, repeated=True)
