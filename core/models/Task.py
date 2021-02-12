class Task:
    def __init__(self, method: str, endpoint: str, headers: dict = None, payload: dict = None):
        self.method = method
        self.endpoint = endpoint
        self.headers = headers
        self.payload = payload
