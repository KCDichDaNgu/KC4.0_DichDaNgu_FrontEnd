


from src.modules.system_setting.database.repository import SystemSettingRepository
from src.modules.system_setting.dtos.system_setting_response import SystemSettingDto
from sys import path
from infrastructure.configs.main import StatusCode, GlobalConfig, get_cnf
from requests import status_codes
from modules.translation_request.database.repository import UserRequestRepository
from typing import Text
from sanic import Blueprint, response
from sanic.response import HTTPResponse
from sanic_openapi import doc


config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG.
STATUS_CODE = config.StatusCode

class create_detect_languege_request:
    text = str
    
class Body:
    data = doc.Object(create_detect_languege_request)

    
@system_setting_bp.post(
    path=APP_CONFIG.ROUTES.system_setting.child.system_setting.path,
    name=APP_CONFIG.ROUTES.system_setting.child.system_setting.name
)
@doc.consumes(Body, location="body")
async def get_system_setting()):
    
    data = request.json['data']

    new_setting = SystemSettingRepository.create_detect_language_task(data)

    if (new_task):
        return response.json(body={
            "code": STATUS_CODES['SUCCESS'],
            "message": "Create task success",
            "data": {
                "taskType": new_task['type'],
                "taskId": str(new_task['id'])
            }
        })
    else:
        return response.json(body={
            "code": STATUS_CODE['FAIL'],
            "message": "Create task fail",
        })
