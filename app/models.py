from sqlmodel import Field, SQLModel

class ExchangeBase(SQLModel):
    name: str

class Exchange(ExchangeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ExchangePublic(ExchangeBase):
    id: int
    