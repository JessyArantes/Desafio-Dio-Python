from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi_pagination import Page, paginate, add_pagination, Params
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "sqlite:///./db.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# MODELS
class Atleta(Base):
    __tablename__ = "atletas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    centro_treinamento = Column(String, nullable=False)
    categoria = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# SCHEMAS
from pydantic import BaseModel

class AtletaCreate(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True


# FASTAPI APP
app = FastAPI(title="API Atletas")

# DEPENDENCY - DB SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ENDPOINTS
@app.post("/atletas", response_model=AtletaResponse)
def criar_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    novo_atleta = Atleta(**atleta.dict())
    db.add(novo_atleta)
    try:
        db.commit()
        db.refresh(novo_atleta)
        return novo_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )

@app.get("/atletas", response_model=Page[AtletaResponse])
def listar_atletas(
    nome: str = Query(None, description="Filtrar por nome"),
    cpf: str = Query(None, description="Filtrar por CPF"),
    db: Session = Depends(get_db),
    params: Params = Depends()
):
    query = db.query(Atleta)

    if nome:
        query = query.filter(Atleta.nome.contains(nome))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)

    atletas = query.all()
    return paginate(atletas, params)


add_pagination(app)
