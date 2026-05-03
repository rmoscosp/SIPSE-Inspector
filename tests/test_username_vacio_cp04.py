from test_base import BaseTest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestUsernameVacio(BaseTest):
    def test_username_vacio(self):
        try:
            logging.info("=== INICIO TEST: USERNAME VACÍO ===")

            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Llenar formulario con username vacío
            logging.info("Llenando formulario con username vacío")
            self.wait.until(EC.presence_of_element_located((By.ID, "regUsername")))
            # NO llenamos username
            self.fill_form(email="juan@email.com", password="Juan12345", role="Tecnico")

            # Enviar
            self.submit_form()

            # Validar mensaje de username obligatorio
            self.wait_for_message("usernameError")
            error_msg = self.get_error_message("usernameError")
            logging.info(f"Mensaje: {error_msg}")
            assert error_msg == "El nombre de usuario es obligatorio."

            # Verificar que no se envió
            reg_msg = self.get_message("regMsg")
            assert reg_msg == "", "El formulario se envió cuando no debía"

            # Verificar persistencia de datos
            logging.info("Verificando que los otros campos conservan valores")
            email_value = self.driver.find_element(By.ID, "regEmail").get_attribute("value")
            password_value = self.driver.find_element(By.ID, "regPassword").get_attribute("value")
            assert email_value == "juan@email.com"
            assert password_value == "Juan12345"

            # Screenshot
            self.take_screenshot("test_username_vacio.png")

            logging.info("=== TEST FINALIZADO OK ===")

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_username_vacio.png")
            raise
        finally:
            self.teardown_method()


if __name__ == "__main__":
    test = TestUsernameVacio()
    test.test_username_vacio()