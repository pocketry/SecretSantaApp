from sqlmodel import Field, SQLModel, Relationship, create_engine

class ExchangeBase(SQLModel):
    name: str


class Exchange(ExchangeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # santaParticipants: list["SantaExchangeParticipation"] = Relationship(back_populates="santa")

class ExchangePublic(ExchangeBase):
    id: int


class SantaBase(SQLModel):
    email: str
    name: str
    parentName: str | None

class Santa(SantaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # exchangeParticipation: list["SantaExchangeParticipation"] = Relationship(back_populates="exchange")


# class SantaExchangeParticipation(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     santaID: int | None = Field(default=None, foreign_key="santa.id")
#     exchangeID: int | None = Field(default=None, foreign_key="exchange.id")
#     isAdmin: bool = Field(default=False)

#     santa: "Santa" = Relationship(back_populates="exchangeParticipation")
#     exchange: "Exchange" = Relationship(back_populates="santaParticipants")

sqlite_file_name = "santas.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":  
    create_db_and_tables()