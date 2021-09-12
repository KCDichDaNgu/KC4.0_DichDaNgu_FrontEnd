from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.system_setting.commands.create_system_setting.http_controller import CreateSystemSetting 

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

system_setting_bp = Blueprint(
    APP_CONFIG.ROUTES['system_setting']['name'], 
    url_prefix=APP_CONFIG.ROUTES['system_setting']['path']
)

system_setting_bp.add_route(
    CreateSystemSetting.as_view(), 
    uri=APP_CONFIG.ROUTES['system_setting.create']['path'],
    methods=[APP_CONFIG.ROUTES['system_setting.create']['method']]
)
