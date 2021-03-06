from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    SmallInteger,
)
from sqlalchemy.orm import relationship

from app.config import settings
from app.db.base_class import Base
from app.models.task import Task  # noqa


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hash = Column(String(settings.STRING_LEN_LIMIT), index=True)
    source = Column(SmallInteger, index=True, nullable=False)
    description = Column(String(settings.STRING_LEN_LIMIT))
    version_num = Column(Integer, index=True, nullable=False)
    result_state = Column(SmallInteger, index=True, nullable=False)

    model_group_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    project_id = Column(Integer, index=True, nullable=False)
    task_id = Column(Integer, index=True, nullable=False)

    # imported/copied model has no mAP
    map = Column(Float, nullable=True)

    related_task = relationship(
        "Task",
        primaryjoin="foreign(Task.id)==Model.task_id",
        backref="result_model",
        uselist=False,
        viewonly=True,
    )

    is_deleted = Column(Boolean, default=False, nullable=False)
    create_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_datetime = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @property
    def group_name(self) -> str:
        return self.group.name  # type: ignore

    @property
    def name(self) -> str:
        return "_".join([self.group_name, str(self.version_num)])
