from test_base import BaseTest
import logging

class TestRegistroExitoso(BaseTest):
    def test_registro_exitoso(self):
        try:
            self.setup_method()
            self.go_to_url()

            # Ir a registro
            self.navigate_to_register()

            # Llenar formulario
            self.fill_form(
                username="juan_usuario1",
                email="juan@empresa.com",
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