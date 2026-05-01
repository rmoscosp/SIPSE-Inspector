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

def test_email_invalido():
    logging.info("=== INICIO TEST: EMAIL INVÁLIDO ===")

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
    # Llenar formulario (email inválido)
    # =========================
    logging.info("Llenando formulario con email inválido")

    wait.until(EC.presence_of_element_located((By.ID, "regUsername"))).send_keys("juan123")
    driver.find_element(By.ID, "regEmail").send_keys("juanemail.com")  # ❌ sin @
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
    # VALIDACIÓN 1: mensaje email
    # =========================
    logging.info("Validando mensaje de error de email")

    wait.until(lambda d: d.find_element(By.ID, "emailError").text != "")

    error_msg = driver.find_element(By.ID, "emailError").text
    logging.info(f"Mensaje: {error_msg}")

    assert "formato válido" in error_msg

    # =========================
    # VALIDACIÓN 2: NO envío
    # =========================
    logging.info("Validando que no se envió")

    reg_msg = driver.find_element(By.ID, "regMsg").text
    assert reg_msg == "", "El formulario se envió cuando no debía"

    # =========================
    # VALIDACIÓN 3: corregir email
    # =========================
    logging.info("Corrigiendo email")

    email_input = driver.find_element(By.ID, "regEmail")
    email_input.clear()
    email_input.send_keys("juan@email.com")

    pause()

    # =========================
    # VALIDACIÓN 4: error desaparece
    # =========================
    logging.info("Verificando que desaparece el error")

    wait.until(lambda d: d.find_element(By.ID, "emailError").text == "")

    error_msg_after = driver.find_element(By.ID, "emailError").text
    assert error_msg_after == "", "El error no desapareció"

    # =========================
    # Screenshot
    # =========================
    driver.save_screenshot("test_email_invalido.png")
    logging.info("Screenshot guardado")

    pause()

    logging.info("=== TEST FINALIZADO OK ===")

    driver.quit()


if __name__ == "__main__":
    test_email_invalido()