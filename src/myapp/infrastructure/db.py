from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import registry

from src.config import Settings

mapper_registry = registry()
Base = mapper_registry.generate_base()


def get_session_factory(engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Database:

    def __init__(
        self,
        settings: Settings,
        echo: bool = False,
        pool_class=NullPool,
    ):
        self.engine = create_engine(
            settings.DATABASE_URL, echo=echo, connect_args=settings.connect_args or {}, poolclass=pool_class
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = Base

    def get_db(self):
        db: Session = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_all(self):
        self.Base.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.Base.metadata.drop_all(bind=self.engine)

    def create_session(self):
        return self.SessionLocal()


# default_db = Database(
#     settings=get_settings(),
# )
