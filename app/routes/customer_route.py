from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.customer_schema import CustomerCreateSchema, CustomerResponseSchema
from app.models.customer import Customer
from app.services import customer_service

bp = Blueprint('customer', __name__)

@bp.post('/create')
@jwt_required()
def create_customer(): 
    data = request.get_json() or {}
    schema = CustomerCreateSchema()
    
    try:
        payload = schema.load(data)
        user_id = get_jwt_identity()
        customer = customer_service.create_customer(
            name=payload["name"],
            phone_number=payload["phone_number"],
            email=payload.get("email"),
            user_id=user_id
        )
    except Exception as exc:
        return jsonify({"Erro": str(exc)}), 400
    
    return jsonify(CustomerResponseSchema().dump(customer)), 201