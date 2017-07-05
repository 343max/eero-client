from abc import abstractproperty

class SessionStorage(object):
    @abstractproperty
    def cookie(self):
        pass
