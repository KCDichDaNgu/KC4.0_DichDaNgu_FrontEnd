


from modules.system_setting.database.repository import SystemSettingRepository
from modules.system_setting.dtos.system_setting_response import SystemSettingDto
from sys import path
from infrastructure.configs.main import StatusCode, GlobalConfig, get_cnf
from requests import status_codes
from typing import Text
from sanic import Blueprint, response
from sanic.response import HTTPResponse
from sanic_openapi import doc

system_setting_bp = Blueprint('system_setting', url_prefix='system-setting')

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG
STATUS_CODE = config.StatusCode

    
@system_setting_bp.get(
    path=APP_CONFIG.ROUTES.system_setting.path,
    name=APP_CONFIG.ROUTES.system_setting.name
)
async def get_system_setting() -> SystemSettingDto:

    current_setting = SystemSettingRepository.find_system_settings()

    if (current_setting):
        return response.json(body={
            "code": STATUS_CODE['SUCCESS'],
            "message": "Create task success",
            "data": current_setting
        })
    else:
        return response.json(body={
            "code": STATUS_CODE['FAIL'],
            "message": "Get setting fail",
        })
