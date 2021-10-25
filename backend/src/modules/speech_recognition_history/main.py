from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.speech_recognition_history.queries.get_single_speech_recognition_history.http_controller import GetSingleSpeechRecognitionHistory

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

speech_recognition_history_bp = Blueprint(
    APP_CONFIG.ROUTES['speech_recognition_history']['name'], 
    url_prefix=APP_CONFIG.ROUTES['speech_recognition_history']['path']
)

speech_recognition_history_bp.add_route(
    GetSingleSpeechRecognitionHistory.as_view(), 
    uri=APP_CONFIG.ROUTES['speech_recognition_history.get_single']['path'],
    methods=[APP_CONFIG.ROUTES['speech_recognition_history.get_single']['method']]
)
