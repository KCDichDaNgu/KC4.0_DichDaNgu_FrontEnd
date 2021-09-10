from sys import path
from infrastructure.configs.main import StatusCode, GlobalConfig, get_cnf
from requests import status_codes
from modules.translation_request.database.repository import UserRequestRepository
from typing import Text
from sanic import Blueprint, response
from sanic.response import HTTPResponse
from sanic_openapi import doc
from main import translation_request_bp


config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG


class create_detect_languege_request:
    text = str

class Body:
    data = doc.Object(create_detect_languege_request)

    
@translation_request_bp.post(
    path=APP_CONFIG.routes.translation_request.child.detect_language.path,
    name=APP_CONFIG.routes.translation_request.child.detect_language.name
)
@doc.consumes(Body, location="body")
async def detect_language_request(request):
    
    data = request.json['data']

    new_task = UserRequestRepository.create_detect_language_task(data)

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
            "code": STATUS_CODES['FAIL'],
            "message": "Create task fail",
        })
