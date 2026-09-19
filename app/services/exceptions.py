"""
Exceções de domínio: o Service lança essas exceções sem saber nada de
HTTP (não sabe o que é status 403, 404, etc). Quem traduz isso para
códigos HTTP é o Controller.
"""

class ValidationError(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class TransactionNotFound(Exception):
    pass


class AccessDenied(Exception):
    pass