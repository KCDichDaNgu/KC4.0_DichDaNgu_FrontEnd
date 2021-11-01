from infrastructure.configs.user import UserRole
from modules.user.domain.entities.user import UserEntity
from modules.user.dtos.get_user_list_response import GetUserListResponse

from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView

from core.middlewares.authentication.core import login_required

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetList(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.database.user.repository import UserRepository
        self.__user_repository = UserRepository()

    @doc.summary(APP_CONFIG.ROUTES['user.get_list']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.get_list']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @doc.consumes(
        doc.String(
            description='firstName',
            name='firstName'
        ),
        location="query")
    @doc.consumes(
        doc.String(
            description='lastName',
            name='last_name'
        ),
        location="query")
    @doc.consumes(
        doc.String(
            description='email',
            name='email'
        ),
        location="query")
    @doc.consumes(
        doc.String(
            description='status',
            name='status'
        ),
        location="query")
    @doc.consumes(
        doc.String(
            description='role',
            name='role'
        ),
        location="query")
    @doc.consumes(
        doc.String(
            description='role',
            name='role'
        ),
        location="query")
    @doc.consumes(
        doc.Integer(
            description='page',
            name='page'
        ),
        location="query"
    )
    @doc.consumes(
        doc.Integer(
            description='perPage',
            name='perPage'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='orderBy',
            name='orderBy'
        ),
        location="query"
    )
    @doc.produces(GetUserListResponse)
    @login_required(roles=[UserRole.admin.value])
    async def get(self, request: Request):
        try:
            first_name = request.args.get('firstName')
            last_name = request.args.get('lastName')
            email = request.args.get('email')
            status = request.args.get('status')
            role = request.args.get('role')
            per_page = request.args.get('perPage')
            page = request.args.get('page')
            order_by = request.args.get('orderBy')

            query = {}
            pagination = {
                'page': 1,
                'per_page': 10
            }

            if not first_name is None:
                query['first_name'] = first_name

            if not last_name is None:
                query['last_name'] = last_name

            if not email is None:
                query['email'] = email

            if not status is None:
                query['status'] = status

            if not role is None:
                query['role'] = role

            if not page is None:
                pagination['page'] = int(page)

            if not per_page is None:
                pagination['per_page'] = int(per_page)

            query_result = await self.__user_repository.find_many_paginated(
                query,
                pagination,
                order_by
            )

            user_list: UserEntity = query_result.data

            users = list(
                map(lambda item: {
                    'id': item.id.value,
                    'username': item.props.username,
                    'firstName': item.props.first_name,
                    'lasttName': item.props.last_name,
                    'password': item.props.password,
                    'avatar': item.props.avatar,
                    'email': item.props.email,
                    'status': item.props.status,
                    'role': item.props.role,
                    'updatedAt': str(item.updated_at.value),
                    'createdAt': str(item.created_at.value),
                }, user_list)
            )
            return response.json(
                body={
                    'code': StatusCodeEnum.success.value,
                    'data': {
                        "per_page": query_result.per_page,
                        "page": query_result.page,
                        "total_entries": query_result.total_entries,
                        "list": users
                    },
                    'message': MESSAGES['success']
                }
            )
    
        except Exception as error:
            print(error)
            return response.json(
                status=500,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
