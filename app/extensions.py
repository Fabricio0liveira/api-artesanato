"""
Instâncias de extensões, criadas SEM app ainda (padrão Application Factory).

Ficam num módulo separado para evitar import circular: models.py importa
`db` daqui, e `app/__init__.py` importa os models — se `db` fosse criado
dentro de `__init__.py`, teríamos um ciclo de import.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()