"""
Configurações da aplicação, separadas por ambiente.

Por que classes e não um único config.py com variáveis soltas?
- Permite trocar de ambiente (dev/test/prod) com uma linha (FLASK_CONFIG=production)
- Evita hardcode de segredos: tudo sensível vem de variável de ambiente
- Facilita testes (banco em memória, CSRF desligado, etc.)
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ConfigBase:
    """Configurações comuns a todos os ambientes."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-nao-use-em-producao")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dev.db')}"
    )


class TestingConfig(ConfigBase):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(ConfigBase):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def init_app(cls, app):
        ConfigBase.init_app(app)
        if not os.environ.get("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL precisa estar definida em produção")
        if os.environ.get("SECRET_KEY", "dev-nao-use-em-producao") == "dev-nao-use-em-producao":
            raise RuntimeError("SECRET_KEY precisa ser definida em produção")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
