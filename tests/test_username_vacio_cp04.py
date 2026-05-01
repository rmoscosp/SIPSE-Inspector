from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

URL = "http://localhost:5500/index.html"
SLOW_MODE = True

def pause():
    if SLOW_MODE:
        time.sleep(1.5)

def test_username_vacio():
    logging.info("=== INICIO TEST: USERNAME VACÍO ===")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    pause()

    # =========================
    # Ir a REGISTER
    # =========================
    logging.info("Ir a registro")
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//p[contains(text(),'Regístrate')]")
    )).click()

    pause()

    # =========================
    # Llenar formulario (username vacío)
    # =========================
    logging.info("Llenando formulario con username vacío")

    wait.until(EC.presence_of_element_located((By.ID, "regUsername")))
    # NO llenamos username

    driver.find_element(By.ID, "regEmail").send_keys("juan@email.com")
    driver.find_element(By.ID, "regPassword").send_keys("Juan12345")
    driver.find_element(By.ID, "regRole").send_keys("Tecnico")

    pause()

    # =========================
    # Click registrar
    # =========================
    logging.info("Intentando registrar")
    driver.find_element(By.XPATH, "//button[contains(text(),'Crear cuenta')]").click()

    pause()

    # =========================
    # VALIDACIÓN 1: mensaje username
    # =========================
    logging.info("Validando mensaje de username obligatorio")

    wait.until(lambda d: d.find_element(By.ID, "usernameError").text != "")

    error_msg = driver.find_element(By.ID, "usernameError").text
    logging.info(f"Mensaje: {error_msg}")

    assert error_msg == "El nombre de usuario es obligatorio."

    # =========================
    # VALIDACIÓN 2: NO envío
    # =========================
    logging.info("Verificando que no se envió")

    reg_msg = driver.find_element(By.ID, "regMsg").text
    assert reg_msg == "", "El formulario se envió cuando no debía"

    # =========================
    # VALIDACIÓN 3: persistencia de datos
    # =========================
    logging.info("Verificando que los otros campos conservan valores")

    email_value = driver.find_element(By.ID, "regEmail").get_attribute("value")
    password_value = driver.find_element(By.ID, "regPassword").get_attribute("value")

    assert email_value == "juan@email.com"
    assert password_value == "Juan12345"

    # =========================
    # Screenshot
    # =========================
    driver.save_screenshot("test_username_vacio.png")
    logging.info("Screenshot guardado")

    pause()

    logging.info("=== TEST FINALIZADO OK ===")

    driver.quit()


if __name__ == "__main__":
    test_username_vacio()