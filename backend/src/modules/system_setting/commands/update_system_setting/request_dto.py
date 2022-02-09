from interface_adapters.interfaces.system_setting.update_system_setting import UpdateSystemSetting
from sanic_openapi import doc

class UpdateSystemSettingDto(UpdateSystemSetting):

    maxUserTextTranslationPerDay: doc.Integer(
        description='Max translate text per day',
        required=True,
    )

    maxUserDocTranslationPerDay: doc.Integer(
        description='Max translate documents per day',
        required=True,
    )
    
    taskExpiredDuration: doc.Integer(
        description='Translation history expire duration',
        required=True,
    )
