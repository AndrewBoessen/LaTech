"""This module defines the SQLAlchemy model for a Job."""

from sqlalchemy import Column, String

from app.database import Base


class Job(Base):
    """The SQLAlchemy model for a job."""

    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    upload_id = Column(String, nullable=True)
    processed_id = Column(String, nullable=True)
    latex_id = Column(String, nullable=True)
    pdf_id = Column(String, nullable=True)
