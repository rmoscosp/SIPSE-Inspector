# SIPSE — Sistema de Registro y Login

Proyecto desarrollado para la asignatura **Pruebas y Métricas de Calidad**. Implementa un módulo de registro e inicio de sesión de usuarios con validaciones de negocio en el backend y pruebas automatizadas E2E con Selenium.

---

## 🗂 Estructura del proyecto

```
pruebas-de-calidad/
├── src/
│   ├── main.py                     # Entrada de la API (FastAPI)
│   ├── index.html                  # Frontend (registro + login)
│   ├── controller/
│   │   └── user_controller.py      # Endpoints: /users/register, /users/login
│   ├── models/
│   │   └── user_model.py           # Modelos Pydantic
│   └── services/
│       └── user_service.py         # Lógica de negocio y validaciones
├── tests/
│   ├── test_registro_exitoso_cp01.py
│   ├── test_registro_fallido_password_cp02.py
│   ├── test_email_invalido_cp03.py
│   ├── test_username_vacio_cp04.py
│   └── test_rol_vacio_cp05.py
└── Pipfile
```

---

## ⚙️ Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Frontend | HTML + JavaScript (vanilla) |
| Pruebas | Selenium WebDriver (Chrome) |
| Entorno virtual | Pipenv |

---

## 🚀 Cómo ejecutar el proyecto

### 1. Activar el entorno virtual

```bash
pipenv shell
```

> Si es la primera vez, instala las dependencias primero con `pipenv install`.

### 2. Levantar el backend

Desde la raíz del proyecto ejecuta:

```bash
pipenv run uvicorn src.main:app --reload
```

Si ya estás dentro de la shell de Pipenv, usa:

```bash
uvicorn src.main:app --reload
```

La API quedará disponible en `http://localhost:8000`. Puedes explorar los endpoints en `http://localhost:8000/docs`.

### 3. Levantar el frontend

Abre una **segunda terminal**, activa el entorno virtual y ejecuta:

```bash
cd src
python -m http.server 5500
```

El frontend estará disponible en `http://localhost:5500/index.html`.

> ⚠️ Es necesario tener **ambos servidores corriendo** antes de ejecutar cualquier prueba.

---

## 🌐 Endpoints de la API

### `POST /users/register`

Registra un nuevo usuario. Aplica las siguientes validaciones:

- `username`: obligatorio, mínimo 3 caracteres
- `email`: obligatorio, formato válido (`usuario@dominio.com`)
- `password`: obligatorio, mínimo 8 caracteres, al menos una mayúscula, una minúscula, un número y un carácter especial (`!@#$%^&*`)
- `role`: obligatorio, debe ser `Admin` o `Tecnico`

### `POST /users/login`

Inicia sesión con email y contraseña. Verifica que el usuario exista y que la contraseña sea correcta.

---

## 🧪 Ejecutar las pruebas

Las pruebas usan **Selenium con Chrome**, por lo que el navegador se abrirá automáticamente y ejecutará cada flujo en pantalla.

### Mejoras implementadas

- ✅ **Estructura modular**: Clase base `BaseTest` con setup/teardown automáticos
- ✅ **Manejo de excepciones**: Try/catch en todos los tests con screenshots de error
- ✅ **Funciones reutilizables**: `fill_form()`, `submit_form()`, `get_error_message()`, etc.
- ✅ **Logging centralizado**: Logs detallados de cada paso
- ✅ **Setup/teardown global**: Inicialización y cierre automático del driver

### Pasos

1. Asegúrate de que el backend (`uvicorn`) y el frontend (`http.server`) estén corriendo.
2. Abre una nueva terminal y activa el entorno virtual:

```bash
pipenv shell
```

3. Entra a la carpeta de pruebas:

```bash
cd tests
```

4. Ejecuta la prueba que desees:

```bash
python test_registro_exitoso_cp01.py
python test_registro_fallido_password_cp02.py
python test_email_invalido_cp03.py
python test_username_vacio_cp04.py
python test_rol_vacio_cp05.py
```

Cada prueba genera logs en consola e, en los casos que aplica, un **screenshot automático** al finalizar. Si falla, se guarda un screenshot de error.

> ⚠️ **Nota**: Para el test CP-01 (registro exitoso), reinicia el backend antes de ejecutarlo si ya hay usuarios registrados en memoria.
---

## 🧾 Análisis de calidad con SonarQube

Se agregó un archivo `sonar-project.properties` en la raíz del proyecto para configurar el análisis.

### Pasos básicos

1. Genera el reporte de cobertura:

```bash
coverage run -m pytest tests/ --tb=no -q
coverage xml -o coverage.xml
```

2. Descarga y extrae SonarScanner CLI en el proyecto (ya está disponible en `sonar-scanner\sonar-scanner-8.0.1.6346`).
3. Crea un token de usuario en SonarQube (UI > Administration > Security > Tokens) y define la variable de entorno `SONAR_TOKEN`.
4. Ejecuta el análisis desde la raíz del proyecto:

```powershell
cd sonar-scanner\sonar-scanner-8.0.1.6346\bin
$env:JAVA_HOME = "<PATH_TO_JDK>"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
cmd /c "sonar-scanner.bat -Dsonar.host.url=http://localhost:9000 -Dsonar.login=%SONAR_TOKEN%"
```

5. Revisa los resultados en el servidor SonarQube en `http://localhost:9000`.

### Scripts útiles

- `run-sonar.ps1`: ejecuta el análisis SonarQube local usando el token y el JDK configurado.
- `export-sonar-results.ps1`: exporta un informe JSON con métricas y análisis recientes desde SonarQube.

### Exportar resultados

Puedes mostrar resultados sin tomar capturas de pantalla usando el script:

```powershell
cd C:\Dev\PruebasYMetricas\SIPSE-Inspector
$env:SONAR_TOKEN = "squ_cae29eb394c9c77078f857ff8107aae053a5ebf8"
.\export-sonar-results.ps1
```

El script genera `sonar-report.json` con las métricas clave y los análisis recientes.

También puedes exportar información directamente desde la UI de SonarQube en `http://localhost:9000`.

---

## 📋 Casos de prueba

| ID | Archivo | Descripción |
|---|---|---|
| CP-01 | `test_registro_exitoso_cp01.py` | Registro exitoso con datos válidos y redirección al login |
| CP-02 | `test_registro_fallido_password_cp02.py` | Contraseña débil: valida indicador "Débil" y mensaje de error |
| CP-03 | `test_email_invalido_cp03.py` | Email sin `@`: valida mensaje de error y que desaparece al corregir |
| CP-04 | `test_username_vacio_cp04.py` | Username vacío: valida mensaje y persistencia de los otros campos |
| CP-05 | `test_rol_vacio_cp05.py` | Rol no seleccionado: valida mensaje y que el formulario no se envía |

---

## 📸 Screenshots

Los casos CP-02 al CP-05 generan automáticamente un screenshot al finalizar la prueba, guardado en la carpeta `tests/`:

- `test_password_debil.png`
- `test_email_invalido.png`
- `test_username_vacio.png`
- `test_rol_vacio.png`
