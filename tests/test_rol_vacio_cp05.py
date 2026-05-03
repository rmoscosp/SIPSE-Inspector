from test_base import BaseTest
import logging
from selenium.webdriver.common.by import By

class TestRolVacio(BaseTest):
    def test_rol_vacio(self):
        try:
            logging.info("=== INICIO TEST: ROL VACÍO ===")

            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Llenar formulario sin seleccionar rol
            logging.info("Llenando formulario sin seleccionar rol")
            self.fill_form(
                username="juan123",
                email="juan@email.com",
                password="Juan12345"
            )

            # Enviar
            self.submit_form()

            # Validar mensaje de rol obligatorio
            self.wait_for_message("roleError")
            error_msg = self.get_error_message("roleError")
            logging.info(f"Mensaje: {error_msg}")
            assert error_msg == "Debe seleccionar un rol."

            # Verificar que no se envió
            reg_msg = self.get_message("regMsg")
            assert reg_msg == "", "El formulario se envió cuando no debía"

            # Verificar que sigue en registro
            assert self.is_element_displayed("registerView")

            # Verificar persistencia de datos
            logging.info("Verificando persistencia de datos")
            email_value = self.driver.find_element(By.ID, "regEmail").get_attribute("value")
            password_value = self.driver.find_element(By.ID, "regPassword").get_attribute("value")
            assert email_value == "juan@email.com"
            assert password_value == "Juan12345"

            # Screenshot
            self.take_screenshot("test_rol_vacio.png")

            logging.info("=== TEST FINALIZADO OK ===")

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_rol_vacio.png")
            raise
        finally:
            self.teardown_method()


if __name__ == "__main__":
    test = TestRolVacio()
    test.test_rol_vacio()