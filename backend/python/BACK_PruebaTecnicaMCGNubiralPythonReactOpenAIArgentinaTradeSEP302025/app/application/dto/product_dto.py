# Example ProductDTO definition
from pydantic import BaseModel

class ProductDTO(BaseModel):
    id: int
    name: str
    description: str
    price: float
    # Add other fields as needed