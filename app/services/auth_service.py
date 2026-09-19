"""
SERVICE: regra de negócio de autenticação. Não conhece `request`,
`jsonify` nem nada de Flask — recebe valores simples, devolve objetos
de domínio ou levanta exceções de domínio.
"""

from app.extensions import db
from app.models.user import User

from app.services.exceptions import ValidationError, InvalidCredentials, UserAlreadyExists


def register_user(email, password):
    email = (email or "").strip().lower()
    
    if not email or not password:
        raise ValidationError("E-mail e Senha são obrigatórios.")
    if len(password) < 6:
        raise ValidationError("Senha precisa ter no mínimo 6 caracteres.")
    if User.query.filter_by(email=email).first():
        raise UserAlreadyExists("Usuário já existe!")

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return user

def authenticate(email, password):
    email = (email or "").strip().lower()
    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        raise InvalidCredentials("Credenciais inválidas!")

    return user