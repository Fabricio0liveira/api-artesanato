"""
CONTROLLER: única camada que conhece Flask (request/jsonify) e o
usuário autenticado da sessão. Fica "fino": recebe a requisição, chama
o Service, formata a resposta com a View e traduz exceções de domínio
em códigos HTTP.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from app.schemas.user_schema import UserRegisterSchema, UserResponseSchema, UserLoginSchema, UserProfileSchema 

from app.models.user import User
from app.services import auth_service
from app.services.exceptions import ValidationError, InvalidCredentials, UserAlreadyExists


bp = Blueprint('auth', __name__)


@bp.post('/register')
def register_user():
    data = request.get_json() or {}
    schema = UserRegisterSchema()
    
    try:
        payload = schema.load(data)
        user = auth_service.register_user(payload["email"], payload["password"])
    except UserAlreadyExists as e:
            return jsonify({"Erro": str(e)}), 400
    except Exception as exc:
        return jsonify({"Erro": exc.messages}), 400
    
    return jsonify(UserResponseSchema().dump(user)), 201


@bp.post('/login')
def login():
    data = request.get_json() or {}
    
    schema = UserLoginSchema()
    try:
        payload = schema.load(data)
    except Exception as exc:
        return jsonify({"Erro": exc.messages}), 400

    try:
        user = auth_service.authenticate(payload["email"], payload["password"])
    except InvalidCredentials as e:
        return jsonify({"Erro": str(e)}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": UserResponseSchema().dump(user)
    }), 200


@bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=str(user_id))
    return jsonify({
        "access_token": new_access_token,
        "token_type": "Bearer"
    }), 200


@bp.post("/logout")
@jwt_required()
def logout():
    return jsonify({"message": "Logout realizado. Remova o token do cliente."}), 200


@bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user is None:
        return jsonify({"Erro": "Usuário não encontrado."}), 404

    return jsonify(UserProfileSchema().dump(user)), 200