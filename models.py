from pydantic import BaseModel, BaseSettings

class Settings(BaseSettings):
    SERVER_NAME: str = "localhost:5000"


class Sales_object(BaseModel):
    partition_key: str
    row_key: str
    finn_code: str
    status: str
    price: int
    expenses: int
    total_price: int
    municipality_tax: int
    boligtype: str
    eierform: str 
    pri_rom: int 
    bolig_areal: int
    bygg_aar: int
    energi_bokstav: str
    energi_farge: str
    tomt_areal: int
    tomt_eieform: str
    gate: str 
    post_nr: int
    post_sted: str
    visninger: list

