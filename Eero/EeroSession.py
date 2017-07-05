from abc import abstractproperty

class EeroSession(object):
    @abstractproperty
    def cookie(self):
        pass
