import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_register_endpoint():
    data = {
        "username": "api_user",
        "email": "api_user@test.com",
        "password": "Password@123",
        "role": "Tecnico"
    }
    
    # Registro exitoso
    response = client.post("/users/register", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario registrado correctamente."
    
    # Registro con error (mismo correo)
    response_dup = client.post("/users/register", json=data)
    assert response_dup.status_code == 400

def test_login_endpoint():
    # Login exitoso (usa el usuario creado en el test anterior)
    data = {
        "email": "api_user@test.com",
        "password": "Password@123"
    }
    response = client.post("/users/login", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Inicio de sesión exitoso."

    # Login fallido
    data_wrong = {
        "email": "api_user@test.com",
        "password": "WrongPassword@123"
    }
    response_wrong = client.post("/users/login", json=data_wrong)
    assert response_wrong.status_code == 400

def test_validation_error_handler():
    # Enviar datos inválidos para probar el manejador de excepciones
    data = {
        "username": "api_user",
        # Falta el email, esto lanzará un RequestValidationError si el controller usa Pydantic
    }
    response = client.post("/users/register", json=data)
    assert response.status_code == 400
    assert "Error en los datos enviados" in response.json()["message"]
