"""
参星（Trinary）- 数据库模型
定义知识图谱的所有实体
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from .database import Base


def generate_uuid():
    """生成 UUID"""
    return str(uuid.uuid4())


class StellarSystem(Base):
    """恒星系统（核心知识单元）"""
    __tablename__ = "stellar_systems"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    star_title = Column(String(500))
    star_summary = Column(Text)
    star_content = Column(Text)

    # 两个独立维度
    lifecycle = Column(
        String(20),
        CheckConstraint("lifecycle IN ('protostar', 'main_sequence', 'red_giant', 'white_dwarf', 'supernova')"),
        default="protostar"
    )
    knowledge_layer = Column(
        String(20),
        CheckConstraint("knowledge_layer IN ('fact', 'decision', 'insight', 'constraint')"),
        default="fact"
    )

    # 属性
    brightness = Column(Float, default=0.5)
    mass = Column(Float, default=0.5)

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    planets = relationship("Planet", back_populates="system", cascade="all, delete-orphan")
    clusters = relationship("Cluster", secondary="system_cluster_map", back_populates="systems")
    history = relationship("SystemHistory", back_populates="system", cascade="all, delete-orphan")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "star_title": self.star_title,
            "star_summary": self.star_summary,
            "star_content": self.star_content,
            "lifecycle": self.lifecycle,
            "knowledge_layer": self.knowledge_layer,
            "brightness": self.brightness,
            "mass": self.mass,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "planets": [p.to_dict() for p in self.planets] if self.planets else [],
        }


class Nebula(Base):
    """星云（知识原料）"""
    __tablename__ = "nebulae"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255))
    content = Column(Text)
    source = Column(String(50))
    density = Column(Float, default=0.1)
    absorbed_by = Column(String(36), ForeignKey("stellar_systems.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "source": self.source,
            "density": self.density,
            "absorbed_by": self.absorbed_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Cluster(Base):
    """星团（知识聚类）"""
    __tablename__ = "clusters"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    type = Column(
        String(20),
        CheckConstraint("type IN ('open', 'globular')"),
        default="open"
    )
    center_system_id = Column(String(36), ForeignKey("stellar_systems.id"), nullable=True)
    density = Column(Float)
    age = Column(String(20))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    systems = relationship("StellarSystem", secondary="system_cluster_map", back_populates="clusters")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "center_system_id": self.center_system_id,
            "density": self.density,
            "age": self.age,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "systems": [s.id for s in self.systems] if self.systems else [],
        }


class SystemClusterMap(Base):
    """恒星系统与星团的多对多关系"""
    __tablename__ = "system_cluster_map"

    system_id = Column(String(36), ForeignKey("stellar_systems.id"), primary_key=True)
    cluster_id = Column(String(36), ForeignKey("clusters.id"), primary_key=True)


class Planet(Base):
    """行星（派生知识）"""
    __tablename__ = "planets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    system_id = Column(String(36), ForeignKey("stellar_systems.id"), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    system = relationship("StellarSystem", back_populates="planets")
    satellites = relationship("Satellite", back_populates="planet", cascade="all, delete-orphan")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "system_id": self.system_id,
            "title": self.title,
            "summary": self.summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "satellites": [s.to_dict() for s in self.satellites] if self.satellites else [],
        }


class Satellite(Base):
    """卫星（细节知识）"""
    __tablename__ = "satellites"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    planet_id = Column(String(36), ForeignKey("planets.id"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    planet = relationship("Planet", back_populates="satellites")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PlanetRelation(Base):
    """行星间关联"""
    __tablename__ = "planet_relations"

    from_planet = Column(String(36), ForeignKey("planets.id"), primary_key=True)
    to_planet = Column(String(36), ForeignKey("planets.id"), primary_key=True)
    relation_type = Column(String(20))


class SystemRelation(Base):
    """恒星系统间关系"""
    __tablename__ = "system_relations"

    from_system = Column(String(36), ForeignKey("stellar_systems.id"), primary_key=True)
    to_system = Column(String(36), ForeignKey("stellar_systems.id"), primary_key=True)
    relation_type = Column(String(20))
    strength = Column(Float, default=0.5)
    direction = Column(String(10), default="bidirectional")


class CosmicWebFiber(Base):
    """宇宙网纤维（跨域关联）"""
    __tablename__ = "cosmic_web_fibers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    from_system = Column(String(36), ForeignKey("stellar_systems.id"), nullable=False)
    to_system = Column(String(36), ForeignKey("stellar_systems.id"), nullable=False)
    fiber_type = Column(
        String(20),
        CheckConstraint("fiber_type IN ('explicit', 'implicit')"),
        default="explicit"
    )
    strength = Column(Float)
    source = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemHistory(Base):
    """历史记录"""
    __tablename__ = "system_history"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    system_id = Column(String(36), ForeignKey("stellar_systems.id"), nullable=False)
    event = Column(String(100))
    detail = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 关系
    system = relationship("StellarSystem", back_populates="history")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "system_id": self.system_id,
            "event": self.event,
            "detail": self.detail,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class EditLog(Base):
    """编辑日志"""
    __tablename__ = "edit_log"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_type = Column(String(50))
    entity_id = Column(String(36))
    user_id = Column(String(100))
    action = Column(String(50))
    detail = Column(Text)
    source = Column(String(10), default="user")
    timestamp = Column(DateTime, default=datetime.utcnow)
