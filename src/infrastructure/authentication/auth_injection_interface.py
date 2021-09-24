from abc import abstractmethod


class AuthInjectionInterface:
    @abstractmethod
    def get_token(self, token):
        raise NotImplementedError()

    @abstractmethod
    def get_deny_token(self, token):
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, token):
        raise NotImplementedError()
    