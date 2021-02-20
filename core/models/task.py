class Task:
    def __init__(self, name: str, method: str, endpoint: str, headers: dict = None, payload: dict = None):
        self.name = name
        self.method = method
        self.endpoint = endpoint
        self.headers = headers
        self.payload = payload
