from typing import Literal
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Contractor API",
    description="Contractor API",
    version="1.0.0",
)

class ContractCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    target: str = Field(min_length=1, max_length=50)
    danger_level: int = Field(ge=1, le=5)
    reward: int = Field(ge=0)
    status: Literal["available", "accepted", "completed"]

contracts: list[dict] = [
    {
        "id": 1,
        "title": "FROM THE PINKERTON DETECTIVE AGENCY",
        "target": "Arthur Morgan",
        "danger_level": 5,
        "reward": 5000,
        "status": "available",
    },
    {
        "id": 2,
        "title": "FOR CRIMES AGAINST THE EMPIRE",
        "target": "Zeb Orrelios",
        "danger_level": 4,
        "reward": 10000,
        "status": "available",
    },
    {
        "id": 3,
        "title": "FROM THE PINKERTON DETECTIVE AGENCY",
        "target": "Dutch Van Der Linde",
        "danger_level": 3,
        "reward": 10000,
        "status": "available",
    },
    {
        "id": 4,
        "title": "WANTED FOR QUESTIONING",
        "target": "Jesse James",
        "danger_level": 4,
        "reward": 7500,
        "status": "completed",
    },
    {
        "id": 5,
        "title": "FOR THEFT OF IMPERIAL PROPERTY",
        "target": "Han Solo",
        "danger_level": 5,
        "reward": 7500,
        "status": "accepted",
    },
]

@app.get("/")
def root():
    return {"message": "Wall of Contracts API is running"}

@app.get("/contracts")
def get_contracts():
    return contracts

@app.get("/contracts/available")
def get_available_contracts():
    available_contracts = []

    for contract in contracts:
        if contract["status"] == "available":
            available_contracts.append(contract)

    return available_contracts

@app.get("/contracts/dangerous")
def get_dangerous_contracts():
    dangerous_contracts = []

    for contract in contracts:
        if contract["danger_level"] >= 4:
            dangerous_contracts.append(contract)

    return dangerous_contracts

@app.get("/contracts/total-reward")
def get_total_reward():
    if contracts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No contracts are available",
        )

    sum_reward: int = 0
    for contract in contracts:
        sum_reward += contract["reward"]

    return sum_reward

@app.get("/contracts/{contract_id}")
def get_contract(contract_id: int):
    for contract in contracts:
        if contract["id"] == contract_id:
            return contract

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contract not found",
    )

@app.post("/contracts", status_code=status.HTTP_201_CREATED)
def create_contract(contract:ContractCreate):
    next_id = max((item["id"] for item in contracts), default=0) + 1

    new_contract ={
        "id": next_id,
        "title": contract.title,
        "target": contract.target,
        "danger_level": contract.danger_level,
        "reward": contract.reward,
        "status": contract.status,
    }

    contracts.append(new_contract)
    return new_contract

@app.post("/contracts/{contract_id}/accept")
def accept_contract(contract_id: int):
    for contract in contracts:
        if contract["id"] == contract_id:

            if contract["status"] != "available":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Contract cannot be accepted because its status is '{contract['status']}'",
                )

            contract["status"] = "accepted"
            return contract
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contract not found",
    )

@app.post("/contracts/{contract_id}/complete")
def complete_contract(contract_id: int):
    for contract in contracts:
        if contract["id"] == contract_id:

            if contract["status"] != "accepted":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Contract cannot be completed because its status is '{contract['status']}'",
                )

            contract["status"] = "completed"
            return contract
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Contract not found",
    )

