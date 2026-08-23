from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.models import Team, User, get_db

app = FastAPI()
router = APIRouter()

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class UserRetrieve(BaseModel):
    id: int
    username: str

@router.post("/signup", response_model=UserRetrieve)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, password=user.password)  # Password should be hashed in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
@router.post("/expenses", response_model=ExpenseRetrieve)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(amount=expense.amount, category=expense.category, date=expense.date, user_id=expense.user_id)
    db.add(db_expense)
    db.commit()  # Commit the transaction to save the expense
    db.refresh(db_expense)
    return db_expense
    return expenses
class Team(BaseModel):
    id: int
    name: str

class TeamCreate(BaseModel):
    name: str

class TeamMember(BaseModel):
    username: str

teams = {}
team_id_counter = 1

@router.post("/teams", response_model=Team)
def create_team(team: TeamCreate):
    global team_id_counter
    new_team = Team(id=team_id_counter, name=team.name)
    teams[team_id_counter] = {"team": new_team, "members": []}
    team_id_counter += 1
    return new_team

@router.post("/teams/{team_id}/invite", response_model=Team)
def invite_member(team_id: int, member: TeamMember):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    teams[team_id]["members"].append(member.username)
    return teams[team_id]["team"]

@router.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams[team_id]["team"]

@router.get("/teams/{team_id}/members")
def get_team_members(team_id: int):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams[team_id]["members"]

app.include_router(router)
