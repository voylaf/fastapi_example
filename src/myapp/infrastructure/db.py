from sqlalchemy.orm import Session, registry, sessionmaker

mapper_registry = registry()
Base = mapper_registry.generate_base()


def get_session_factory(engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Database:
    def __init__(self, engine):
        self.SessionLocal = sessionmaker(bind=engine)

    def create_session(self) -> Session:
        return self.SessionLocal()

    def create_all(self):
        self.Base.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.Base.metadata.drop_all(bind=self.engine)


# default_db = Database(
#     settings=get_settings(),
# )
