from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEAFULT_RENDERER_CLASSES
    
