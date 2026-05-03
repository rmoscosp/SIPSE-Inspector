from test_base import BaseTest
import logging

class TestPasswordDebil(BaseTest):
    def test_password_debil(self):
        try:
            logging.info("=== INICIO TEST: PASSWORD DÉBIL ===")

            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Llenar formulario con password débil
            self.fill_form(
                username="juan123",
                email="juan@email.com",
                password="abc",
                role="Tecnico"
            )

            # Enviar
            self.submit_form()

            # Validar indicador de contraseña débil
            self.wait_for_message("passwordStrength")
            strength = self.get_message("passwordStrength")
            logging.info(f"Indicador: {strength}")
            assert strength == "Débil", f"Esperado 'Débil', obtuvo: {strength}"

            # Validar mensaje de error
            error_msg = self.get_error_message("passwordError")
            logging.info(f"Mensaje error: {error_msg}")
            assert "mínimo 8 caracteres" in error_msg

            # Verificar que no se envió el formulario
            reg_msg = self.get_message("regMsg")
            assert reg_msg == "", "El formulario se envió cuando no debía"

            # Verificar que sigue en registro
            assert self.is_element_displayed("registerView")

            # Screenshot final
            self.take_screenshot("test_password_debil.png")

            logging.info("=== TEST FINALIZADO OK ===")

        except Exception as e:
            logging.error(f"Test falló: {e}")
            self.take_screenshot("error_password_debil.png")
            raise
        finally:
            self.teardown_method()


if __name__ == "__main__":
    test = TestPasswordDebil()
    test.test_password_debil()