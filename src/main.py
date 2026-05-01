from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from controller.user_controller import router as user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="SIPSE API")

app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []

    for err in exc.errors():
        campo = err["loc"][-1]
        errores.append(f"Error en el campo '{campo}'.")

    return JSONResponse(
        status_code=400,
        content={
            "message": "Error en los datos enviados.",
            "errors": errores
        }
    )