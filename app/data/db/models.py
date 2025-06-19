from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telefono = Column(String, nullable=False)
    registro = Column(DateTime, nullable=False)

    imagenes = relationship("ImageModel", back_populates="usuario")


class MaterialModel(Base):
    __tablename__ = "clasificacion_materiales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_material = Column(String, nullable=False)
    tipo_material = Column(String, nullable=False)
    renovable = Column(Boolean, default=False)
    reciclable = Column(Boolean, default=False)
    confianza = Column(Float, nullable=False)  # <- ARREGLADO
    impacto_ambiental = Column(String)
    imagen = Column(UUID(as_uuid=True), ForeignKey("imagenes.id"))

class ImageModel(Base):
    __tablename__ = "imagenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_imagen = Column(String, nullable=False)
    ruta = Column(String, nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    fecha = Column(DateTime, nullable=False)
    usuario = relationship("UserModel", back_populates="imagenes")
    modelo_id = Column(UUID(as_uuid=True), ForeignKey("desempeno_modelo.id"))

class ModelPerformanceModel(Base):
    __tablename__ = "desempeno_modelo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    formato = Column(String, nullable=False)
    score = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    dataset = Column(String)
    fecha_entrenamiento = Column(DateTime)
    optimizado = Column(Boolean, default=False)
