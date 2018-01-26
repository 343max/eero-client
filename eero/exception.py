class ClientException(Exception):
    def __init__(self, status, error_message):
        super(ClientException, self).__init__()
        self.status = status
        self.error_message = error_message
