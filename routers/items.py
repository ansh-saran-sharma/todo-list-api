# Imports
import models, schemas
from typing import List
from sqlalchemy.orm import Session
from database_connection import get_db
from fastapi import HTTPException, status, Depends, APIRouter

# Initializing APIRouter object
# Replacing "@app." with "@router."
router = APIRouter(
    tags=["TODO Items"] # Grouping of routes 
)

# Retrieving All Items
@router.get("/get-all-items", response_model=List[schemas.OutItem]) # "response_model" defines what data is to be sent back to the user. List[reponse_model] is used since multiple objects/data/orm_model are being returned instead of 1.
async def all_users(db: Session = Depends(get_db)):
    # Query to retireve/get all items/rows and executing it with ".all()"
    all_items = db.query(models.Item).all()
    return all_items

# Retrieving specific Item
@router.get("/get-item/{id}", response_model=schemas.OutItem) # "response_model" defines what data is to be sent back to the user.
async def get_one_users(id: int, db: Session = Depends(get_db)):
    # Query to fetch first item/row with matching id and executing it with ".first()"
    specific_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not specific_item:
        # Raising an HTPException if no item/row is found with the input id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id: {id} does not exists.")
    return specific_item

# Creating Item
@router.post("/add-item", status_code=status.HTTP_201_CREATED, response_model=schemas.OutItem) # Defining default status code to be returned upon successfully adding an item
async def add_item(input_data: schemas.Item, db: Session = Depends(get_db)):
    # Creating new entry
    new_item = models.Item(**input_data.dict()) # Converting the Pydantic Model/Schema to Python Dictionary and then Unpacking it.
    # Adding/Pushing new entry into the Database
    db.add(new_item)
    # Committing changes to Database
    db.commit()
    # Retrieving the new item/entry
    db.refresh(new_item)
    return new_item

# Deleting Item
@router.delete("/delete-item/{id}", status_code=status.HTTP_204_NO_CONTENT) # Defining default status code to be returned upon successfully deleting an item
async def delete_item(id: int, db: Session = Depends(get_db)):
    # Query to fetch first item/row with matching id
    query = db.query(models.Item).filter(models.Item.id == id)
    # Executing query with ".first()" and checking if any such item/row exists
    if query.first() == None:
        raise HTTPException(status_code=404, detail=f"Item with id: {id} does not exists.")
    # Deleting item/row
    query.delete(synchronize_session=False)
    # Committing changes to Database
    db.commit()

# Updating Item
@router.put("/update-item/{id}", response_model=schemas.OutItem) # "response_model" defines what data is to be sent back to the user.
async def update_item(id: int, user_input: schemas.Item, db: Session = Depends(get_db)):
    # Query to fetch first item/row with matching id
    query = db.query(models.Item).filter(models.Item.id == id)
    # Executing query with ".first()" and checking if any such item/row exists
    if query.first() == None:
        raise HTTPException(status_code=404, detail=f"Item with id: {id} could not be updated.")
    # Updating item/row
    query.update(user_input.dict(), synchronize_session=False)
    # Committing changes to Database
    db.commit()
    # Returning updated item/row
    return query.first()