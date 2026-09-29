import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..auth import create_access_token, get_user_id_from_request, hash_password, verify_password
from ..config import MAX_UPLOAD_MB
from ..database import get_db
from ..models import User, Recommendation
from ..schemas import RegisterRequest, LoginRequest, HomeRequest, PartyRequest, JewelryRequest
from ..services.recommendation_service import create_recommendation

router = APIRouter(prefix="/api")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def require_user(request, db):
    uid = get_user_id_from_request(request)
    user = db.get(User, uid) if uid else None
    if not user: raise HTTPException(401, "Authentication required")
    return user

@router.post("/register")
def register(payload: RegisterRequest, db: Session=Depends(get_db)):
    email = payload.email.strip().lower()
    if db.query(User).filter(User.email==email).first():
        raise HTTPException(409, "Email already registered")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    response = JSONResponse({"message":"Registration successful"})
    response.set_cookie("access_token", create_access_token(user.id), httponly=True, samesite="lax", max_age=43200)
    return response

@router.post("/login")
def login(payload: LoginRequest, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.email==payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    response = JSONResponse({"message":"Login successful"})
    response.set_cookie("access_token", create_access_token(user.id), httponly=True, samesite="lax", max_age=43200)
    return response

@router.post("/logout")
def logout():
    response = JSONResponse({"message":"Logged out"})
    response.delete_cookie("access_token")
    return response

@router.get("/health")
def health():
    return {"status":"ok","service":"PocketSmart AI"}

@router.get("/session-info")
def session_info(request: Request, db: Session=Depends(get_db)):
    uid = get_user_id_from_request(request)
    user = db.get(User, uid) if uid else None
    if not user: return {"authenticated":False}
    return {"authenticated":True,"user_id":user.id,"name":user.name,"email":user.email}

@router.get("/session-data")
def session_data(request: Request, db: Session=Depends(get_db)):
    user = require_user(request, db)
    count = db.query(Recommendation).filter(Recommendation.user_id==user.id).count()
    return {"user_id":user.id,"recommendation_count":count}

@router.post("/generate-home")
def generate_home(payload: HomeRequest, request: Request, db: Session=Depends(get_db)):
    user = require_user(request, db)
    return create_recommendation(db,user.id,"home",payload.model_dump())

@router.post("/generate-party")
def generate_party(payload: PartyRequest, request: Request, db: Session=Depends(get_db)):
    user = require_user(request, db)
    return create_recommendation(db,user.id,"party",payload.model_dump())

@router.post("/generate-jewelry")
async def generate_jewelry(request: Request, budget: float, occasion: str, style: str="Elegant",
                           notes: str="", outfit: UploadFile|None=File(default=None),
                           db: Session=Depends(get_db)):
    user = require_user(request, db)
    payload = JewelryRequest(budget=budget, occasion=occasion, style=style, notes=notes)
    image_path = None
    if outfit and outfit.filename:
        if outfit.content_type not in {"image/jpeg","image/png","image/webp"}:
            raise HTTPException(415, "Only JPEG, PNG or WEBP images are allowed")
        data = await outfit.read()
        if len(data) > MAX_UPLOAD_MB*1024*1024:
            raise HTTPException(413, f"Image must be <= {MAX_UPLOAD_MB} MB")
        suffix = Path(outfit.filename).suffix.lower() or ".jpg"
        image_path = str(UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}")
        Path(image_path).write_bytes(data)
    try:
        return create_recommendation(db,user.id,"jewelry",payload.model_dump(),image_path)
    finally:
        if image_path: Path(image_path).unlink(missing_ok=True)

@router.get("/history")
def history(request: Request, db: Session=Depends(get_db)):
    user = require_user(request, db)
    rows = db.query(Recommendation).filter(Recommendation.user_id==user.id).order_by(Recommendation.created_at.desc()).all()
    return [{"id":r.id,"planner":r.planner,"budget":r.budget,"request":r.request_json,
             "result":r.result_json,"created_at":r.created_at.isoformat()} for r in rows]

@router.get("/recommendations/{recommendation_id}")
def details(recommendation_id: int, request: Request, db: Session=Depends(get_db)):
    user = require_user(request, db)
    r = db.query(Recommendation).filter(Recommendation.id==recommendation_id, Recommendation.user_id==user.id).first()
    if not r: raise HTTPException(404, "Recommendation not found")
    return {"id":r.id,"planner":r.planner,"budget":r.budget,"request":r.request_json,
            "result":r.result_json,"created_at":r.created_at.isoformat()}
