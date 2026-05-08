import uuid
from test_base import BaseTest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestRegistroExitoso(BaseTest):
    def test_registro_exitoso(self):
        try:
            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Datos únicos para evitar duplicados
            unique_id = uuid.uuid4().hex[:6]
            username = f"juan_usuario_{unique_id}"
            email = f"juan{unique_id}@empresa.com"

            # Llenar formulario
            self.fill_form(
                username=username,
                email=email,
                password="Juan@12345",
                role="Tecnico"
            )

            # Enviar
            self.submit_form()

            # Esperar mensaje
            self.wait_for_message("regMsg")

            mensaje = self.get_message("regMsg")

            print("MENSAJE:", mensaje)

            assert "Registro exitoso" in mensaje, f"Mensaje inesperado: {mensaje}"

            # Verificar redirección a login
            self.wait.until(EC.visibility_of_element_located((By.ID, "loginView")))
            assert self.is_element_displayed("loginView"), "No se redirigió a login"

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_registro_exitoso.png")
            raise
        finally:
            self.teardown_method()


if __name__ == "__main__":
    test = TestRegistroExitoso()
    test.test_registro_exitoso()