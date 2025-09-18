"""
Some custom errors to have some flavour
"""


class DatabaseError(Exception):
    """Raised when an unexpected error happens when performing a query, and we probably don't want to handle it"""

    def __init__(
        self,
        query: str,
        params: tuple,
        root_cause: Exception,
        base_msg="unexpected fatal error when performing query",
    ):
        self.sql = query
        self.params = params
        self.root_cause = root_cause
        self.message = (
            f"{base_msg}\nQuery: {query}\nParams: {params}\nCause: {root_cause}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"DatabaseError: {self.message}"


class NonFatalDatabaseError(DatabaseError):
    """Raised when an unexpected error happens when performing a query, and we probably  want to handle it"""

    def __init__(
        self,
        query: str,
        params: tuple,
        root_cause: Exception,
        base_msg="unexpected error when performing query",
    ):
        super().__init__(query, params, root_cause, base_msg)

    def __str__(self):
        return f"DatabaseError: {self.message}"


class MissingItemException(Exception):
    """Raised when we expected something, but we didn't find it"""

    def __init__(self, message="cannot find expected item"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"MissingItemException: {self.message}"


class ScrappingError(Exception):
    """Raised when an error happens while scrapping"""

    def __init__(self, message: str, root: Exception):
        self.message = f"Error scrapping: {message} | Root cause: {root}"
        self.root = root
        super().__init__(self.message)

    def __str__(self):
        return f"ScrappingError: {self.message}"

class FatalErrorException(Exception):
    """Raised when we expected something, we don't like what we got instead, and we want everybody to just die"""

    def __init__(self, message="everything went pizdetz"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"FatalErrorException: {self.message}"
