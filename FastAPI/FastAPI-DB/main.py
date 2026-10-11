from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Contract, Mercenary
from connection import Base, engine, SessionLocal

# =========================
# PYDANTIC SCHEMAS
# =========================

class ContractCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=2, max_length=500)
    difficulty: int = Field(ge=1, le=10)
    reward: float = Field(gt=0)
    district: str = Field(min_length=2, max_length=100)


class ContractUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(
        default=None, min_length=2, max_length=500
    )
    difficulty: int | None = Field(default=None, ge=1, le=10)
    reward: float | None = Field(default=None, gt=0)
    district: str | None = Field(
        default=None, min_length=2, max_length=100
    )


class ContractRead(BaseModel):
    id: int
    name: str
    description: str
    difficulty: int
    reward: float
    district: str
    status: str
    mercenary_id: int | None

    model_config = ConfigDict(from_attributes=True)


class MercenaryCreate(BaseModel):
    nickname: str = Field(min_length=2, max_length=50)
    level: int = Field(ge=1)
    reputation: int = Field(default=0, ge=0)
    balance: float = Field(default=0, ge=0)


class MercenaryRead(BaseModel):
    id: int
    nickname: str
    level: int
    reputation: int
    balance: float

    model_config = ConfigDict(from_attributes=True)


class ContractTake(BaseModel):
    mercenary_id: int = Field(gt=0)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


# =========================
# APPLICATION
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Contract Management API",
    description=(
        "Contract management, mercenary assignment, "
        "contract lifecycle and profitability ranking."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Contract Management API is running"}


# =========================
# CONTRACT CRUD
# =========================

@app.post(
    "/contracts",
    response_model=ContractRead,
    status_code=status.HTTP_201_CREATED,
)
def create_contract(data: ContractCreate, db: DbSession):
    contract = Contract(**data.model_dump())

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return contract


@app.get("/contracts", response_model=list[ContractRead])
def get_contracts(
    db: DbSession,
    contract_status: str | None = Query(
        default=None,
        alias="status",
        pattern="^(OPEN|IN_PROGRESS|COMPLETED|FAILED)$",
    ),
    district: str | None = None,
    min_reward: float | None = Query(default=None, ult=None, ge=0),
    max_difficulty: int | None = Query(defage=1, le=10),
):
    statement = select(Contract)

    if contract_status is not None:
        statement = statement.where(
            Contract.status == contract_status
        )

    if district is not None:
        statement = statement.where(
            Contract.district == district
        )

    if min_reward is not None:
        statement = statement.where(
            Contract.reward >= min_reward
        )

    if max_difficulty is not None:
        statement = statement.where(
            Contract.difficulty <= max_difficulty
        )

    return db.scalars(statement).all()


@app.get("/contracts/best-value", response_model=ContractRead)
def get_best_contract(db: DbSession):
    statement = (
        select(Contract)
        .where(Contract.status == "OPEN")
        .order_by(
            (Contract.reward / Contract.difficulty).desc(),
            Contract.id.asc(),
        )
        .limit(1)
    )

    contract = db.scalar(statement)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No open contracts available",
        )

    return contract


@app.get("/contracts/{contract_id}", response_model=ContractRead)
def get_contract(contract_id: int, db: DbSession):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    return contract


@app.patch("/contracts/{contract_id}", response_model=ContractRead)
def update_contract(
    contract_id: int,
    data: ContractUpdate,
    db: DbSession,
):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    changes = data.model_dump(exclude_unset=True)

    for field_name, value in changes.items():
        setattr(contract, field_name, value)

    db.commit()
    db.refresh(contract)

    return contract


@app.delete(
    "/contracts/{contract_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_contract(contract_id: int, db: DbSession):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    if contract.status == "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a contract in progress",
        )

    db.delete(contract)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================
# CONTRACT BUSINESS LOGIC
# =========================

@app.post(
    "/contracts/{contract_id}/take",
    response_model=ContractRead,
)
def take_contract(
    contract_id: int,
    data: ContractTake,
    db: DbSession,
):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    if contract.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only open contracts can be taken",
        )

    mercenary = db.get(Mercenary, data.mercenary_id)

    if mercenary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mercenary not found",
        )

    if contract.difficulty > mercenary.level:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contract difficulty exceeds mercenary level",
        )

    contract.mercenary_id = mercenary.id
    contract.status = "IN_PROGRESS"

    db.commit()
    db.refresh(contract)

    return contract


@app.post(
    "/contracts/{contract_id}/complete",
    response_model=ContractRead,
)
def complete_contract(contract_id: int, db: DbSession):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    if contract.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only contracts in progress can be completed",
        )

    if contract.mercenary_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contract has no assigned mercenary",
        )

    mercenary = db.get(Mercenary, contract.mercenary_id)

    if mercenary is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Assigned mercenary does not exist",
        )

    contract.status = "COMPLETED"
    mercenary.balance += contract.reward

    db.commit()
    db.refresh(contract)

    return contract


@app.post(
    "/contracts/{contract_id}/fail",
    response_model=ContractRead,
)
def fail_contract(contract_id: int, db: DbSession):
    contract = db.get(Contract, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found",
        )

    if contract.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only contracts in progress can fail",
        )

    contract.status = "FAILED"

    db.commit()
    db.refresh(contract)

    return contract


# =========================
# MERCENARY ENDPOINTS
# =========================

@app.post(
    "/mercenaries",
    response_model=MercenaryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_mercenary(data: MercenaryCreate, db: DbSession):
    existing = db.scalar(
        select(Mercenary).where(
            Mercenary.nickname == data.nickname
        )
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mercenary nickname already exists",
        )

    mercenary = Mercenary(**data.model_dump())

    db.add(mercenary)
    db.commit()
    db.refresh(mercenary)

    return mercenary


@app.get("/mercenaries", response_model=list[MercenaryRead])
def get_mercenaries(db: DbSession):
    statement = select(Mercenary).order_by(Mercenary.id)

    return db.scalars(statement).all()


@app.get(
    "/mercenaries/{mercenary_id}",
    response_model=MercenaryRead,
)
def get_mercenary_by_id(mercenary_id: int, db: DbSession):
    mercenary = db.get(Mercenary, mercenary_id)

    if mercenary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mercenary not found",
        )

    return mercenary