class GenericError(Exception):
    def __init__(self, error_code: int, message: str) -> None:
        self.code = error_code
        self.message = message
        super().__init__(self.message)

