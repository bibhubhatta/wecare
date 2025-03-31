from typing import List, Optional

from sqlalchemy import (
    Column,
    Engine,
    Integer,
    MetaData,
    Table,
    Text,
    create_engine,
    insert,
    inspect,
    select,
)

from .client_dashboard import ClientDashboard, ClientDashboardRepository


class ClientDashboardRepositorySql(ClientDashboardRepository):
    @staticmethod
    def from_sqlalchemy_db_url(url: str) -> "ClientDashboardRepositorySql":
        engine = create_engine(url)
        return ClientDashboardRepositorySql(engine)

    table = Table(
        "ClientDashboard",
        MetaData(),
        Column("client_id", Integer, primary_key=True),
        Column("html", Text, nullable=False),
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

    def save(self, dashboard: ClientDashboard) -> None:
        """Save client dashboard to database"""
        with self.engine.connect() as conn:
            # Check if dashboard already exists
            stmt = select(self.table).where(
                self.table.c.client_id == dashboard.client_id
            )
            result = conn.execute(stmt).fetchone()

            if result:
                # Update existing dashboard
                stmt = (
                    self.table.update()
                    .where(self.table.c.client_id == dashboard.client_id)
                    .values(html=dashboard.html)
                )
            else:
                # Insert new dashboard
                stmt = insert(self.table).values(
                    client_id=dashboard.client_id, html=dashboard.html
                )

            conn.execute(stmt)
            conn.commit()

    def get(self, client_id: int) -> Optional[ClientDashboard]:
        """Get dashboard by client ID"""
        with self.engine.connect() as conn:
            stmt = select(self.table).where(self.table.c.client_id == client_id)
            result = conn.execute(stmt).fetchone()

            if not result:
                return None

            return ClientDashboard(html=result.html)

    def get_all(self) -> List[ClientDashboard]:
        """Get all dashboards"""
        with self.engine.connect() as conn:
            stmt = select(self.table)
            results = conn.execute(stmt).fetchall()

            dashboards = []
            for row in results:
                dashboards.append(ClientDashboard(html=row.html))

            return dashboards
