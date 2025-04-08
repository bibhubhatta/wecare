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

from . import VisitEditPageRepository
from .visit_edit_page import VisitEditPage


class VisitEditPageRepositorySql(VisitEditPageRepository):
    @staticmethod
    def from_sqlalchemy_db_url(url: str) -> "VisitEditPageRepositorySql":
        engine = create_engine(url)
        return VisitEditPageRepositorySql(engine)

    table = Table(
        "VisitEditPage",
        MetaData(),
        Column("visit_id", Integer, primary_key=True),
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

    def save(self, visit_page: VisitEditPage) -> None:
        """Save visit edit page to database"""
        with self.engine.connect() as conn:
            # Check if visit page already exists
            stmt = select(self.table).where(
                self.table.c.visit_id == visit_page.visit_id
            )
            result = conn.execute(stmt).fetchone()

            if result:
                # Update existing visit page
                stmt = (
                    self.table.update()
                    .where(self.table.c.visit_id == visit_page.visit_id)
                    .values(html=visit_page.html)
                )
            else:
                # Insert new visit page
                stmt = insert(self.table).values(
                    visit_id=visit_page.visit_id, html=visit_page.html
                )

            conn.execute(stmt)
            conn.commit()

    def get(self, visit_id: int) -> Optional[VisitEditPage]:
        """Get visit page by visit ID"""
        with self.engine.connect() as conn:
            stmt = select(self.table).where(self.table.c.visit_id == visit_id)
            result = conn.execute(stmt).fetchone()

            if not result:
                return None

            return VisitEditPage(html=result.html)

    def get_all(self) -> List[VisitEditPage]:
        """Get all visit pages"""
        with self.engine.connect() as conn:
            stmt = select(self.table)
            results = conn.execute(stmt).fetchall()

            visit_pages = []
            for row in results:
                visit_pages.append(VisitEditPage(html=row.html))

            return visit_pages

    def __contains__(self, visit_id: int) -> bool:
        """Check if a visit ID exists in the repository"""
        with self.engine.connect() as conn:
            stmt = select(self.table).where(self.table.c.visit_id == visit_id)
            result = conn.execute(stmt).fetchone()
            return result is not None
