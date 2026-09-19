"""
CONTROLLER: única camada que conhece Flask (request/jsonify) e o
usuário autenticado da sessão. Fica "fino": recebe a requisição, chama
o Service, formata a resposta com a View e traduz exceções de domínio
em códigos HTTP.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required

from app.services import auth_service
from app.services.exceptions import ValidationError, InvalidCredentials, UserAlreadyExists
 

bp = Blueprint('auth', __name__)

@bp.post('/register')
def register_user():
    data = request.get_json() or {}
    try:
        user = auth_service.register_user(data.get("email"), data.get("password"))
    except ValidationError as e:
        return jsonify({"Erro": str(e)}), 400
    except UserAlreadyExists as e:
        return jsonify({"Erro": str(e)}), 400 

    return jsonify({"id": user.id, "email": user.email}), 201

@bp.post('/login')
def login():
    data = request.get_json() or {}
    try:
        user = auth_service.authenticate(data.get("email"), data.get("password"))
    except InvalidCredentials as e:
        return jsonify({"Erro": str(e)}), 401

    login_user(user)
    return jsonify({"message": f"Bem vindo, {user.email}"}), 200

@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado"}), 200