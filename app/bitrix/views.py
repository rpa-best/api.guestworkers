from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .authentication import TokenAuthentication
from .logger import logger
from .tasks import update_contact

class BitrixWebHook(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, *args, **kwargs):
        logger.debug(str(f'Request data: {request.data}'))
        event = request.data.get('event')
        contact_id = request.data.get("data", {}).get("FIELDS", {}).get("ID")
        if event == 'ONCRMCONTACTUPDATE' and contact_id:
            logger.info(f"Контакт {contact_id} был обновлён")
            update_contact.delay(contact_id)
        return Response({'status': 'ok'})
