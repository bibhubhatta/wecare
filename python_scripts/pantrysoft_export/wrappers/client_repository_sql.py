import json
from typing import List, Optional

from sqlalchemy import (
    Column,
    Engine,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    inspect,
    select,
)

from .client import Client, ClientRepository


class ClientRepositorySql(ClientRepository):
    @staticmethod
    def from_sqlalchemy_db_url(url: str) -> "ClientRepositorySql":
        engine = create_engine(url)
        return ClientRepositorySql(engine)

    table = Table(
        "Client",
        MetaData(),
        Column("id", Integer, primary_key=True),
        Column("json", String, nullable=False),
    )

    def __init__(self, engine: Engine):
        self.engine = engine
        self.metadata = MetaData()

        inspector = inspect(self.engine)
        if not inspector.has_table(self.table.name):
            # Create the table if it doesn't exist
            self.table.create(self.engine)
        else:
            # Verify the existing columns match expected schema
            columns = inspector.get_columns(self.table.name)
            column_names = {col["name"] for col in columns}
            expected_columns = {col.name for col in self.table.columns}

            if column_names != expected_columns:
                missing = expected_columns - column_names
                extra = column_names - expected_columns
                error_msg = []
                if missing:
                    error_msg.append(f"Missing columns: {', '.join(missing)}")
                if extra:
                    error_msg.append(f"Unexpected columns: {', '.join(extra)}")
                raise ValueError(f"Table schema mismatch: {'; '.join(error_msg)}")

    def save(self, client: Client) -> None:
        """Save client to database"""
        with self.engine.connect() as conn:
            # Check if client already exists
            stmt = select(self.table).where(self.table.c.id == client.id)
            result = conn.execute(stmt).fetchone()

            if result:
                # Update existing client
                stmt = (
                    self.table.update()
                    .where(self.table.c.id == client.id)
                    .values(json=json.dumps(client.client_dict))
                )
            else:
                # Insert new client
                stmt = insert(self.table).values(
                    id=client.id, json=json.dumps(client.client_dict)
                )

            conn.execute(stmt)
            conn.commit()

    def get(self, client_id: int) -> Optional[Client]:
        """Get client by ID"""
        with self.engine.connect() as conn:
            stmt = select(self.table).where(self.table.c.id == client_id)
            result = conn.execute(stmt).fetchone()

            if not result:
                return None

            client_dict = json.loads(result.json)
            return Client(client_dict=client_dict)

    def get_all(self) -> List[Client]:
        """Get all clients"""
        with self.engine.connect() as conn:
            stmt = select(self.table)
            results = conn.execute(stmt).fetchall()

            clients = []
            for row in results:
                client_dict = json.loads(row.json)
                clients.append(Client(client_dict=client_dict))

            return clients
