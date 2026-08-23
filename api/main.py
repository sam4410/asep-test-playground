from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from db.models import Task, User, Product
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
router = APIRouter()

app = FastAPI()
router = APIRouter()

@router.get("/api/v1/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    stock_quantity: int
    category_id: int

@router.post("/api/v1/admin/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

app.include_router(router)
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

class Task(BaseModel):
    id: int
    title: str
    description: str
    assignee_id: int
    status: str
    created_at: int
    updated_at: int

class TaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int

@router.post("/api/v1/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Validate assignee exists
    assignee = db.query(User).filter(User.id == task.assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    db_task = Task(
        title=task.title,
        description=task.description,
        assignee_id=task.assignee_id,
        status="todo",  # Default status
        created_at=int(datetime.now().timestamp()),  # Store as Unix timestamp
        updated_at=int(datetime.now().timestamp())   # Store as Unix timestamp
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/api/v1/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/api/v1/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@router.put("/api/v1/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.assignee_id = task.assignee_id
    db_task.updated_at = int(datetime.now().timestamp())
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/api/v1/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}

@router.post("/api/v1/products", response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/api/v1/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/api/v1/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/api/v1/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

app.include_router(router)
