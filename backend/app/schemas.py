"""
参星（Trinary）- Pydantic 模式
定义 API 请求和响应的数据结构
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# 恒星系统模式
class StellarSystemBase(BaseModel):
    """恒星系统基础模式"""
    name: str = Field(..., description="系统名称")
    star_title: Optional[str] = Field(None, description="知识标题")
    star_summary: Optional[str] = Field(None, description="知识摘要")
    star_content: Optional[str] = Field(None, description="原始内容")
    lifecycle: Optional[str] = Field("protostar", description="生命周期")
    knowledge_layer: Optional[str] = Field("fact", description="知识层次")
    brightness: Optional[float] = Field(0.5, description="知识活跃度")
    mass: Optional[float] = Field(0.5, description="知识权重")


class StellarSystemCreate(StellarSystemBase):
    """创建恒星系统请求"""
    pass


class StellarSystemUpdate(BaseModel):
    """更新恒星系统请求"""
    name: Optional[str] = None
    star_title: Optional[str] = None
    star_summary: Optional[str] = None
    star_content: Optional[str] = None
    lifecycle: Optional[str] = None
    knowledge_layer: Optional[str] = None
    brightness: Optional[float] = None
    mass: Optional[float] = None


class StellarSystemResponse(StellarSystemBase):
    """恒星系统响应"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    planets: List["PlanetResponse"] = []

    class Config:
        from_attributes = True


# 行星模式
class PlanetBase(BaseModel):
    """行星基础模式"""
    title: str = Field(..., description="派生知识标题")
    summary: Optional[str] = Field(None, description="派生知识摘要")


class PlanetCreate(PlanetBase):
    """创建行星请求"""
    system_id: str


class PlanetResponse(PlanetBase):
    """行星响应"""
    id: str
    system_id: str
    created_at: Optional[datetime] = None
    satellites: List["SatelliteResponse"] = []

    class Config:
        from_attributes = True


# 卫星模式
class SatelliteBase(BaseModel):
    """卫星基础模式"""
    content: str = Field(..., description="细节知识内容")


class SatelliteCreate(SatelliteBase):
    """创建卫星请求"""
    planet_id: str


class SatelliteResponse(SatelliteBase):
    """卫星响应"""
    id: str
    planet_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 星云模式
class NebulaBase(BaseModel):
    """星云基础模式"""
    name: Optional[str] = Field(None, description="星云名称")
    content: str = Field(..., description="原始内容")
    source: Optional[str] = Field(None, description="来源")
    density: Optional[float] = Field(0.1, description="聚合密度")


class NebulaCreate(NebulaBase):
    """创建星云请求"""
    pass


class NebulaResponse(NebulaBase):
    """星云响应"""
    id: str
    absorbed_by: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 星团模式
class ClusterBase(BaseModel):
    """星团基础模式"""
    name: str = Field(..., description="星团名称")
    type: Optional[str] = Field("open", description="星团类型")
    center_system_id: Optional[str] = Field(None, description="核心恒星系统")
    density: Optional[float] = Field(None, description="聚合密度")
    age: Optional[str] = Field(None, description="年龄")
    status: Optional[str] = Field("active", description="状态")


class ClusterCreate(ClusterBase):
    """创建星团请求"""
    pass


class ClusterResponse(ClusterBase):
    """星团响应"""
    id: str
    created_at: Optional[datetime] = None
    systems: List["StellarSystemResponse"] = []

    class Config:
        from_attributes = True


# 关系模式
class SystemRelationCreate(BaseModel):
    """创建恒星系统间关系请求"""
    from_system: str
    to_system: str
    relation_type: Optional[str] = None
    strength: Optional[float] = 0.5
    direction: Optional[str] = "bidirectional"


class SystemRelationResponse(SystemRelationCreate):
    """恒星系统间关系响应"""
    pass


class CosmicWebFiberCreate(BaseModel):
    """创建宇宙网纤维请求"""
    from_system: str
    to_system: str
    fiber_type: Optional[str] = "explicit"
    strength: Optional[float] = None
    source: Optional[str] = None


class CosmicWebFiberResponse(CosmicWebFiberCreate):
    """宇宙网纤维响应"""
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 历史记录模式
class HistoryResponse(BaseModel):
    """历史记录响应"""
    id: str
    system_id: str
    event: str
    detail: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True


# 星系全景模式
class GalaxyResponse(BaseModel):
    """星系全景响应"""
    systems: List[StellarSystemResponse]
    clusters: List[ClusterResponse]
    nebulae: List[NebulaResponse]
    relations: List[SystemRelationResponse]
    fibers: List[CosmicWebFiberResponse]


# 搜索模式
class SearchRequest(BaseModel):
    """搜索请求"""
    q: str = Field(..., description="搜索关键词")
    type: Optional[str] = Field(None, description="搜索类型")
    lifecycle: Optional[str] = Field(None, description="生命周期筛选")
    knowledge_layer: Optional[str] = Field(None, description="知识层次筛选")


class SearchResponse(BaseModel):
    """搜索响应"""
    systems: List[StellarSystemResponse]
    nebulae: List[NebulaResponse]
    total: int


# 解决 forward reference
ClusterResponse.model_rebuild()
StellarSystemResponse.model_rebuild()
