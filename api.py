import endpoints
import constants
import messages
import queries

import protorpc
from protorpc import remote
from protorpc import message_types

user = endpoints.get_current_user()


@endpoints.api(name='dhs-hw', version='v1',
               allowed_client_ids=constants.CLIENT_IDS, scopes=[endpoints.EMAIL_SCOPE])
class MobileAPI(remote.Service):

    @endpoints.method(messages.TasksRequest, messages.Tasks,
                      path='get_task_list', http_method='GET',
                      name='get_task_list')
    def get_task_list(self, request):
        tasks = queries.get_tasks(request.group, user, request.task_done)
        tasks_msg = []
        for task in tasks:
            task_msg = messages.Task(
                    subject = task.subject,
                    type = task.type
                )
            if task.extra_title:
                task_msg.extra_title = task.extra_title

            tasks_msg.append(task_msg)

        return messages.Tasks(tasks=tasks_msg)

    @endpoints.method(messages.TaskRequest, messages.Task,
                      path='get_task_list', http_method='GET',
                      name='get_task_list')
    def get_task(self, request):
        urlid = request.urlid
        task = queries.get_task(urlid, user)
        if task:
            task_msg = messages.Task(
                subject = task.subject,
                type = task.type,
                time_added = task.time_added,
                task_done = task.task_done
            )
