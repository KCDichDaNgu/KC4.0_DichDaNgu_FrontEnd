from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.speech_recognition_request.command.create_speech_recognition_request.http_controller import CreateSpeechRecognitionRequest

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

speech_recognition_request_bp = Blueprint(
    APP_CONFIG.ROUTES['speech_recognition_request']['name'], 
    url_prefix=APP_CONFIG.ROUTES['speech_recognition_request']['path']
)

speech_recognition_request_bp.add_route(
    CreateSpeechRecognitionRequest.as_view(), 
    uri=APP_CONFIG.ROUTES['speech_recognition_request.create']['path'],
    methods=[APP_CONFIG.ROUTES['speech_recognition_request.create']['method']]
)
