from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates import templates
from app.auth import login_user, logout_user, check_credentials

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login(request: Request, error: str | None = None):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error}
    )

@router.post("/api/login", response_class=RedirectResponse)
def login(username: str = Form(), password: str = Form()):
    if not check_credentials(username, password):
        return RedirectResponse(
            "/login?error=wrong",
                status_code=302
            )

    response = RedirectResponse(
        "/dashboard",
        status_code=302
    )
    login_user(response, username)
    return response

@router.post("/api/logout")
def logout(request: Request):
    response = RedirectResponse(
        "/login",
        status_code=302
    )
    logout_user(response, request)
    return response