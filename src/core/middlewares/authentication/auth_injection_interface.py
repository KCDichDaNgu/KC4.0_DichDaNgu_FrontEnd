from abc import abstractmethod


class AuthInjectionInterface:

    @abstractmethod
    def get_token(self, access_token):
        raise NotImplementedError()

    @abstractmethod
    def delete_token(self, access_token):
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, access_token):
        raise NotImplementedError()
    