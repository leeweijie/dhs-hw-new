import endpoints
import constants
import messages

import protorpc
from protorpc import remote
from protorpc import message_types

user = endpoints.get_current_user()

@endpoints.api(name='dhs-hw', version='v1', scopes=[endpoints.EMAIL_SCOPE], allowed_client_ids=constants.CLIENT_IDS)
class MobileAPI(remote.Service):
    @endpoints.method(message_types.VoidMessage, messages.Tasks,
                      path='get_task_list', http_method='GET',
                      name='get_task_list')
    def get_task_list(self, request):
