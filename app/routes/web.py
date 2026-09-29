from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import get_user_id_from_request
from ..database import get_db
from ..models import User, Recommendation

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def current_user(request, db):
    uid = get_user_id_from_request(request)
    return db.get(User, uid) if uid else None


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": current_user(request, db)}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    history = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "history": history
        }
    )


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner_page(
    planner: str,
    request: Request,
    db: Session = Depends(get_db)
):
    if planner not in {"home", "party", "jewelry"}:
        return RedirectResponse("/", status_code=303)

    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={
            "user": user,
            "planner": planner
        }
    )


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    rows = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "user": user,
            "history": rows
        }
    )