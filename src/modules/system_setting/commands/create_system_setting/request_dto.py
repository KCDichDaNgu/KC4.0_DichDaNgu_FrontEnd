from interface_adapters.interfaces.system_setting.create_system_setting import CreateSystemSetting
from sanic_openapi import doc


class CreateSystemSettingDto(CreateSystemSetting):

    # editorId: doc.UUID(
    #     description='Source text',
    #     required=True
    # )

    maxTranslateTextPerDay: doc.Integer(
        description='Max translate text per day',
        required=True,
    )

    maxTranslateDocPerDay: doc.Integer(
        description='Max translate documents per day',
        required=True,
    )
    
    translationHistoryExpireDuration: doc.Integer(
        description='Translation history expire duration',
        required=True,
    )
