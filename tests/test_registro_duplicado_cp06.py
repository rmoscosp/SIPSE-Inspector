import uuid
from test_base import BaseTest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestRegistroDuplicado(BaseTest):
    def test_registro_duplicado(self):
        try:
            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Usar un correo fijo para provocar duplicado
            email = "usuario_duplicado@empresa.com"
            username1 = "user_dup_1"
            username2 = "user_dup_2"

            # Primer registro (debería ser exitoso)
            self.fill_form(username=username1, email=email, password="Password@123", role="Tecnico")
            self.submit_form()
            self.wait_for_message("regMsg")
            
            # Navegar de nuevo al registro si nos redirigió al login
            self.wait.until(EC.visibility_of_element_located((By.ID, "loginView")))
            self.driver.find_element(By.XPATH, "//p[contains(text(),'Regístrate')]").click()

            # Segundo registro con el mismo correo
            self.fill_form(username=username2, email=email, password="Password@123", role="Admin")
            self.submit_form()

            # Esperar mensaje de error
            self.wait.until(EC.visibility_of_element_located((By.ID, "regMsg")))
            mensaje = self.get_message("regMsg")

            print("MENSAJE:", mensaje)

            assert "Ya existe un usuario registrado con ese correo" in mensaje, f"Mensaje inesperado: {mensaje}"

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_registro_duplicado.png")
            raise
        finally:
            self.teardown_method()

if __name__ == "__main__":
    test = TestRegistroDuplicado()
    test.test_registro_duplicado()
