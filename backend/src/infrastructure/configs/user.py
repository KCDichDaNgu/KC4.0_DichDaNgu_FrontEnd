from core.types import ExtendedEnum 

class UserStatus(str, ExtendedEnum):
    active = 'active'
    inactive = 'inactive'

class UserRole(str, ExtendedEnum):
    admin = 'admin'
    member = 'member'

class UserQuota(int, ExtendedEnum):
    text_translation_quota = 100
    audio_translation_quota = 1000