import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración global de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BaseTest:
    def setup_method(self, method=None):
        """Inicializa variables, el driver y el wait"""
        self.url = "http://localhost:5500/index.html"
        self.slow_mode = True
        self.driver = None
        self.wait = None

        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            logging.info("Driver inicializado correctamente")
        except Exception as e:
            logging.error(f"Error al inicializar driver: {e}")
            raise

    def teardown_method(self, method=None):
        """Cierra el driver"""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Driver cerrado correctamente")
            except Exception as e:
                logging.error(f"Error al cerrar driver: {e}")

    def pause(self):
        """Pausa opcional para modo lento"""
        if self.slow_mode:
            time.sleep(1.5)

    def navigate_to_register(self):
        """Navega a la vista de registro"""
        try:
            logging.info("Navegando a registro")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//p[contains(text(),'Regístrate')]")
            )).click()
            self.pause()
        except Exception as e:
            logging.error(f"Error al navegar a registro: {e}")
            raise

    def fill_form(self, username="", email="", password="", role=""):
        """Llena el formulario de registro"""
        try:
            logging.info("Llenando formulario")
            if username:
                self.wait.until(EC.presence_of_element_located((By.ID, "regUsername"))).send_keys(username)
            if email:
                self.driver.find_element(By.ID, "regEmail").send_keys(email)
            if password:
                self.driver.find_element(By.ID, "regPassword").send_keys(password)
            if role:
                self.driver.find_element(By.ID, "regRole").send_keys(role)
            self.pause()
        except Exception as e:
            logging.error(f"Error al llenar formulario: {e}")
            raise

    def submit_form(self):
        """Envía el formulario"""
        try:
            logging.info("Enviando formulario")
            self.pause()
            self.driver.find_element(By.XPATH, "//button[contains(text(),'Crear cuenta')]").click()
        except Exception as e:
            logging.error(f"Error al enviar formulario: {e}")
            raise

    def get_error_message(self, element_id):
        """Obtiene mensaje de error de un elemento"""
        try:
            return self.driver.find_element(By.ID, element_id).text
        except Exception as e:
            logging.error(f"Error al obtener mensaje de error de {element_id}: {e}")
            return ""

    def get_message(self, element_id):
        """Obtiene mensaje general"""
        try:
            return self.driver.find_element(By.ID, element_id).text
        except Exception as e:
            logging.error(f"Error al obtener mensaje de {element_id}: {e}")
            return ""

    def wait_for_message(self, element_id):
        """Espera a que aparezca un mensaje"""
        try:
            self.wait.until(lambda d: d.find_element(By.ID, element_id).text != "")
        except Exception as e:
            logging.error(f"Error esperando mensaje en {element_id}: {e}")
            raise

    def is_element_displayed(self, element_id):
        """Verifica si un elemento está visible"""
        try:
            return self.driver.find_element(By.ID, element_id).is_displayed()
        except Exception as e:
            logging.error(f"Error verificando visibilidad de {element_id}: {e}")
            return False

    def take_screenshot(self, filename):
        """Toma screenshot"""
        try:
            self.driver.save_screenshot(filename)
            logging.info(f"Screenshot guardado: {filename}")
        except Exception as e:
            logging.error(f"Error al tomar screenshot {filename}: {e}")

    def go_to_url(self):
        """Navega a la URL principal"""
        try:
            self.driver.get(self.url)
        except Exception as e:
            logging.error(f"Error al navegar a {self.url}: {e}")
            raise