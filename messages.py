from protorpc import messages
from protorpc import message_types


class Task(messages.Message):
    name = messages.StringField(required=True)
    time_added = message_types.DateTimeField()

    subject = messages.StringField(required=True)
    is_private = messages.BooleanField(default=False, required=True)
    due_date = message_types.DateTimeField()
    time_needed = messages.IntegerField()
    priority = messages.IntegerField()

    task_done = messages.BooleanField(required=True)


class SubjectCombination(messages.Message):
    subject_combination = messages.StringField(repeated=True)