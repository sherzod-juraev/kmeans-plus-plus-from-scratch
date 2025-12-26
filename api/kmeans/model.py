from datetime import datetime, timezone
from sqlalchemy import Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid, \
    JSONB, ARRAY
from uuid import uuid4, UUID
from database import Base


class KmeansData(Base):
    __tablename__ = 'kmeans_data'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    n_clusters: Mapped[int] = mapped_column(Integer, nullable=False)
    preprocessing: Mapped[dict] = mapped_column(JSONB, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    chat_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    chat: Mapped['Chat'] = relationship(
        'Chat',
        back_populates='kmeans_datas',
        foreign_keys=[chat_id],
        lazy='noload'
    )


    kmeans_centroid: Mapped['KmeansCentroid'] = relationship(
        'KmeansCentroid',
        back_populates='kmeans_data',
        foreign_keys='KmeansCentroid.kmeans_data_id',
        passive_deletes=True,
        lazy='noload'
    )


class KmeansCentroid(Base):
    __tablename__ = 'kmeans_centroids'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    values: Mapped[list[list[float]]] = mapped_column(ARRAY(Float), nullable=False)
    fit_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    fit_time: Mapped[float] = mapped_column(Float, nullable=False)
    kmeans_data_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('kmeans_data.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    kmeans_data: Mapped['KmeansData'] = relationship(
        'KmeansData',
        back_populates='kmeans_centroid',
        foreign_keys=[kmeans_data_id],
        lazy='selectin'
    )