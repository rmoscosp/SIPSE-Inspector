from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# =========================
# CONFIG LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "http://localhost:5500/index.html"

SLOW_MODE = True

def pause():
    if SLOW_MODE:
        time.sleep(1.5)

def test_password_debil():
    logging.info("=== INICIO TEST: PASSWORD DÉBIL ===")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    pause()

    # =========================
    # Ir a REGISTER
    # =========================
    logging.info("Navegando a registro")
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//p[contains(text(),'Regístrate')]")
    )).click()

    pause()

    # =========================
    # Llenar formulario
    # =========================
    logging.info("Llenando formulario con password débil")

    wait.until(EC.presence_of_element_located((By.ID, "regUsername"))).send_keys("juan123")
    driver.find_element(By.ID, "regEmail").send_keys("juan@email.com")
    driver.find_element(By.ID, "regPassword").send_keys("abc")
    driver.find_element(By.ID, "regRole").send_keys("Tecnico")

    pause()

    # =========================
    # Click registrar
    # =========================
    logging.info("Intentando registrar usuario")
    driver.find_element(By.XPATH, "//button[contains(text(),'Crear cuenta')]").click()

    pause()

    # =========================
    # VALIDACIÓN 1
    # =========================
    logging.info("Validando indicador de contraseña débil")

    wait.until(lambda d: d.find_element(By.ID, "passwordStrength").text != "")

    strength = driver.find_element(By.ID, "passwordStrength").text
    logging.info(f"Indicador: {strength}")

    assert strength == "Débil", f"Esperado 'Débil', obtuvo: {strength}"

    # =========================
    # VALIDACIÓN 2
    # =========================
    logging.info("Validando mensaje de error")

    error_msg = driver.find_element(By.ID, "passwordError").text
    logging.info(f"Mensaje error: {error_msg}")

    assert "mínimo 8 caracteres" in error_msg

    # =========================
    # VALIDACIÓN 3
    # =========================
    logging.info("Verificando que no se envió el formulario")

    reg_msg = driver.find_element(By.ID, "regMsg").text
    assert reg_msg == "", "El formulario se envió cuando no debía"

    # =========================
    # VALIDACIÓN 4
    # =========================
    logging.info("Verificando que sigue en registro")

    assert driver.find_element(By.ID, "registerView").is_displayed()

    # =========================
    # SCREENSHOT FINAL
    # =========================
    driver.save_screenshot("test_password_debil.png")
    logging.info("Screenshot guardado: test_password_debil.png")

    pause()

    logging.info("=== TEST FINALIZADO OK ===")

    driver.quit()


if __name__ == "__main__":
    test_password_debil()