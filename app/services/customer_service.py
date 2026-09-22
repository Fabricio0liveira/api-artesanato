from app.extensions import db
from app.models.customer import Customer
from app.models.user import User

def create_customer(name, phone_number, email, user_id):
    email = (email or "").strip().lower()
    phone_number = (phone_number or "").strip()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise ValueError("Usuário não encontrado.")

    existing_phone = Customer.query.filter_by(phone_number=phone_number).first()
    if existing_phone:
        raise ValueError("Número de telefone já cadastrado para outro cliente.")

    if email:
        existing_email = Customer.query.filter_by(email=email).first()
        if existing_email:
            raise ValueError("Email já cadastrado para outro cliente.")
    else:
        email = None

    customer = Customer(name=name, phone_number=phone_number, email=email, user_id=user_id)
    db.session.add(customer)
    db.session.commit()

    return customer
