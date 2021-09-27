from core.types import ExtendedEnum 

class UserStatus(str, ExtendedEnum):
    active = 'active'
    inactive = 'inactive'

class UserRole(str, ExtendedEnum):
    admin = 'admin'
    member = 'member'