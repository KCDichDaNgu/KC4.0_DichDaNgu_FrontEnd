from modules.translation_history.queries.get_translation_history_by_id.http_controller import GetTranslationHistoryById
from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.translation_history.queries.get_single_translation_history.http_controller import GetSingleTranslationHistory

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

translation_history_bp = Blueprint(
    APP_CONFIG.ROUTES['translation_history']['name'], 
    url_prefix=APP_CONFIG.ROUTES['translation_history']['path']
)

translation_history_bp.add_route(
    GetSingleTranslationHistory.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_history.get_single']['path'],
    methods=[APP_CONFIG.ROUTES['translation_history.get_single']['method']]
)

translation_history_bp.add_route(
    GetTranslationHistoryById.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_history.get']['path'],
    methods=[APP_CONFIG.ROUTES['translation_history.get']['method']]
)
