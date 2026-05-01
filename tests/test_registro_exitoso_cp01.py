from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIG
URL = "http://localhost:5500/index.html"

def test_registro_exitoso():
    driver = webdriver.Chrome()
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    # Ir a registro
    wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'Regístrate')]"))).click()

    # Llenar formulario
    wait.until(EC.presence_of_element_located((By.ID, "regUsername"))).send_keys("juan_usuario1")
    driver.find_element(By.ID, "regEmail").send_keys("juan@empresa.com")
    driver.find_element(By.ID, "regPassword").send_keys("Juan@12345")
    driver.find_element(By.ID, "regRole").send_keys("Tecnico")

    # Enviar
    driver.find_element(By.XPATH, "//button[contains(text(),'Crear cuenta')]").click()

    wait.until(lambda d: d.find_element(By.ID, "regMsg").text != "")

    mensaje = driver.find_element(By.ID, "regMsg").text

    print("MENSAJE:", mensaje)

    assert "Registro exitoso" in mensaje, f"Mensaje inesperado: {mensaje}"

    wait.until(lambda d: d.find_element(By.ID, "loginView").is_displayed())

    driver.quit()


if __name__ == "__main__":
    test_registro_exitoso()