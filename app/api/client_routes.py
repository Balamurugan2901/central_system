from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import get_db
from app.database.models import Client
from app.models.client_schema import ClientCreate, ClientResponse

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.ip_address == client.ip_address).first()
    if existing:
        raise HTTPException(status_code=400, detail="IP address already registered")

    new_client = Client(
        name=client.name,
        ip_address=client.ip_address
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": "Client deleted successfully"}
