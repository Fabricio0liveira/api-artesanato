from flask import Flask, jsonify

from config import config
from app.extensions import db, login_manager, migrate


def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    _registrar_extensoes(app)
    _registrar_controllers(app)
    #_registrar_error_handlers(app)

    return app


def _registrar_extensoes(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


def _registrar_controllers(app):
    # "Controllers" no lugar de "blueprints de rotas" — mesma mecânica do
    # Flask (Blueprint), só que aqui cada arquivo é tratado como o C do MVC.
    #from app.controllers.auth_controller import bp as auth_bp
    from app.routes.index import bp as health_bp

    #app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(health_bp, url_prefix="/api")
    

'''
def _registrar_error_handlers(app):
    @app.errorhandler(404)
    def nao_encontrado(erro):
        return jsonify({"erro": "recurso não encontrado"}), 404

    @app.errorhandler(500)
    def erro_interno(erro):
        db.session.rollback()
        return jsonify({"erro": "erro interno do servidor"}), 500
'''
