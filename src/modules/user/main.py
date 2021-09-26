from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.user.queries.me.http_controller import GetMe
from modules.user.commands.auth.http_controller import Auth
from modules.user.commands.logout.http_controller import Logout

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

user_bp = Blueprint(
    APP_CONFIG.ROUTES['user']['name'], 
    url_prefix=APP_CONFIG.ROUTES['user']['path']
)

user_bp.add_route(
    GetMe.as_view(), 
    uri=APP_CONFIG.ROUTES['user.me']['path'],
    methods=[APP_CONFIG.ROUTES['user.me']['method']]
)

user_bp.add_route(
    Auth.as_view(), 
    uri=APP_CONFIG.ROUTES['user.auth']['path'],
    methods=[APP_CONFIG.ROUTES['user.auth']['method']]
)

user_bp.add_route(
    Logout.as_view(), 
    uri=APP_CONFIG.ROUTES['user.logout']['path'],
    methods=[APP_CONFIG.ROUTES['user.logout']['method']]
)

