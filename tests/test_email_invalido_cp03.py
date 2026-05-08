from test_base import BaseTest
import logging
from selenium.webdriver.common.by import By

class TestEmailInvalido(BaseTest):
    def test_email_invalido(self):
        try:
            logging.info("=== INICIO TEST: EMAIL INVÁLIDO ===")

            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Llenar formulario con email inválido
            self.fill_form(
                username="juan123",
                email="juanemail.com",
                password="Juan12345",
                role="Tecnico"
            )

            # Enviar
            self.submit_form()

            # Validar mensaje de error de email
            self.wait_for_message("emailError")
            error_msg = self.get_error_message("emailError")
            logging.info(f"Mensaje: {error_msg}")
            assert "formato válido" in error_msg

            # Validar que no se envió
            reg_msg = self.get_message("regMsg")
            assert reg_msg == "", "El formulario se envió cuando no debía"

            # Corregir email
            logging.info("Corrigiendo email")
            email_input = self.driver.find_element(By.ID, "regEmail")
            email_input.clear()
            email_input.send_keys("juan@email.com")
            self.pause()

            # Verificar que desaparece el error
            logging.info("Verificando que desaparece el error")
            self.wait.until(lambda d: d.find_element(By.ID, "emailError").text == "")
            error_msg_after = self.get_error_message("emailError")
            assert error_msg_after == "", "El error no desapareció"

            # Screenshot
            self.take_screenshot("test_email_invalido.png")

            logging.info("=== TEST FINALIZADO OK ===")

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_email_invalido.png")
            raise
        finally:
            self.teardown_method()


if __name__ == "__main__":
    test = TestEmailInvalido()
    test.test_email_invalido()