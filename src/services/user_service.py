import bcrypt
import re

usuarios_db = []
ROLES_VALIDOS = ["Admin", "Tecnico"]

class UserService:

    @staticmethod
    def validar_campos_obligatorios(data):
        if not data.username:
            raise ValueError("El campo 'username' es obligatorio.")
        if not data.email:
            raise ValueError("El campo 'email' es obligatorio.")
        if not data.password:
            raise ValueError("El campo 'password' es obligatorio.")
        if not data.role:
            raise ValueError("El campo 'role' es obligatorio.")

    @staticmethod
    def validar_username(username):
        if len(username.strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")

    @staticmethod
    def validar_email(email):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, email):
            raise ValueError("El correo electrónico no tiene un formato válido.")

    @staticmethod
    def validar_password(password):
        if len(password) < 8:
            raise ValueError("La contraseña debe tener mínimo 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r'\d', password):
            raise ValueError("La contraseña debe incluir al menos un número.")
        if not re.search(r'[!@#$%^&*]', password):
            raise ValueError("La contraseña debe incluir al menos un carácter especial (!@#$%^&*).")

    @staticmethod
    def validar_rol(role):
        if role not in ROLES_VALIDOS:
            raise ValueError(f"El rol debe ser uno de: {ROLES_VALIDOS}.")

    @staticmethod
    def register(data):
        # RF-01
        UserService.validar_campos_obligatorios(data)

        # RF-02
        UserService.validar_username(data.username)

        # RF-03
        UserService.validar_email(data.email)

        # RF-04
        UserService.validar_password(data.password)

        # RF-05
        UserService.validar_rol(data.role)

        # duplicado
        if any(u["email"] == data.email for u in usuarios_db):
            raise ValueError("Ya existe un usuario registrado con ese correo.")

        # RF-06
        password_hash = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        usuarios_db.append({
            "username": data.username,
            "email": data.email,
            "password": password_hash,
            "role": data.role
        })

        return {"message": "Usuario registrado correctamente."}

    @staticmethod
    def login(data):
        if not data.email:
            raise ValueError("El campo 'email' es obligatorio.")
        if not data.password:
            raise ValueError("El campo 'password' es obligatorio.")

        UserService.validar_email(data.email)

        usuario = next((u for u in usuarios_db if u["email"] == data.email), None)

        if not usuario:
            raise ValueError("No existe un usuario con ese correo.")

        if not bcrypt.checkpw(data.password.encode(), usuario["password"]):
            raise ValueError("La contraseña ingresada es incorrecta.")

        if not usuario.get("role"):
            raise ValueError("El usuario no tiene un rol asignado.")

        return {
            "message": "Inicio de sesión exitoso.",
            "user": usuario["username"],
            "role": usuario["role"]
        }
