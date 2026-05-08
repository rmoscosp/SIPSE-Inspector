import pytest
from src.services.user_service import UserService, usuarios_db

@pytest.fixture(autouse=True)
def reset_db():
    usuarios_db.clear()

def test_validar_campos_obligatorios():
    class DummyData:
        username = "user"
        email = "test@test.com"
        password = "Password@1"
        role = "Admin"
    
    data = DummyData()
    UserService.validar_campos_obligatorios(data)
    
    data.username = ""
    with pytest.raises(ValueError, match="El campo 'username' es obligatorio."):
        UserService.validar_campos_obligatorios(data)

def test_validar_username():
    UserService.validar_username("user123")
    with pytest.raises(ValueError, match="El nombre de usuario debe tener al menos 3 caracteres."):
        UserService.validar_username("ab")

def test_validar_email():
    UserService.validar_email("correo@valido.com")
    with pytest.raises(ValueError, match="El correo electrónico no tiene un formato válido."):
        UserService.validar_email("correoinvalido")

def test_validar_password():
    UserService.validar_password("Password@123")
    
    with pytest.raises(ValueError, match="La contraseña debe tener mínimo 8 caracteres."):
        UserService.validar_password("Pass@1")

def test_validar_rol():
    UserService.validar_rol("Admin")
    UserService.validar_rol("Tecnico")
    with pytest.raises(ValueError, match="El rol debe ser uno de:"):
        UserService.validar_rol("Invitado")

def test_register_and_login():
    class DummyData:
        username = "testuser"
        email = "test@domain.com"
        password = "Password@123"
        role = "Admin"

    data = DummyData()
    
    # Registro exitoso
    res = UserService.register(data)
    assert res["message"] == "Usuario registrado correctamente."
    assert len(usuarios_db) == 1
    
    # Registro duplicado
    with pytest.raises(ValueError, match="Ya existe un usuario registrado con ese correo."):
        UserService.register(data)
        
    # Login exitoso
    res_login = UserService.login(data)
    assert res_login["message"] == "Inicio de sesión exitoso."
    assert res_login["user"] == "testuser"
    assert res_login["role"] == "Admin"
    
    # Login fallido por contraseña incorrecta
    class WrongPasswordData:
        email = "test@domain.com"
        password = "WrongPassword@123"
        
    with pytest.raises(ValueError, match="La contraseña ingresada es incorrecta."):
        UserService.login(WrongPasswordData())

    # Login fallido por usuario no existe
    class NotFoundData:
        email = "notfound@domain.com"
        password = "Password@123"
        
    with pytest.raises(ValueError, match="No existe un usuario con ese correo."):
        UserService.login(NotFoundData())
