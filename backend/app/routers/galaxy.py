"""
参星（Trinary）- 星系 API
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import (
    StellarSystem,
    Nebula,
    Cluster,
    SystemRelation,
    CosmicWebFiber,
    Planet,
)
from ..schemas import (
    StellarSystemResponse,
    NebulaResponse,
    ClusterResponse,
    SystemRelationResponse,
    CosmicWebFiberResponse,
    GalaxyResponse,
    SearchResponse,
    SystemRelationCreate,
    CosmicWebFiberCreate,
)

router = APIRouter()


@router.get("/", response_model=GalaxyResponse)
async def get_galaxy(
    db: AsyncSession = Depends(get_db),
):
    """获取星系全景"""
    # 获取所有恒星系统（预加载行星和卫星）
    systems_result = await db.execute(
        select(StellarSystem).options(
            selectinload(StellarSystem.planets).selectinload(Planet.satellites)
        )
    )
    systems = systems_result.scalars().unique().all()

    # 获取所有星团（预加载系统）
    clusters_result = await db.execute(
        select(Cluster).options(selectinload(Cluster.systems))
    )
    clusters = clusters_result.scalars().unique().all()

    # 获取所有星云
    nebulae_result = await db.execute(select(Nebula))
    nebulae = nebulae_result.scalars().all()

    # 获取所有关系
    relations_result = await db.execute(select(SystemRelation))
    relations = relations_result.scalars().all()

    # 获取所有宇宙网纤维
    fibers_result = await db.execute(select(CosmicWebFiber))
    fibers = fibers_result.scalars().all()

    return GalaxyResponse(
        systems=systems,
        clusters=clusters,
        nebulae=nebulae,
        relations=relations,
        fibers=fibers,
    )


@router.get("/search", response_model=SearchResponse)
async def search_galaxy(
    q: str = Query(..., description="搜索关键词"),
    type: Optional[str] = Query(None, description="搜索类型"),
    lifecycle: Optional[str] = Query(None, description="生命周期筛选"),
    knowledge_layer: Optional[str] = Query(None, description="知识层次筛选"),
    db: AsyncSession = Depends(get_db),
):
    """搜索星系"""
    # 搜索恒星系统
    systems_query = select(StellarSystem).where(
        or_(
            StellarSystem.name.ilike(f"%{q}%"),
            StellarSystem.star_title.ilike(f"%{q}%"),
            StellarSystem.star_summary.ilike(f"%{q}%"),
            StellarSystem.star_content.ilike(f"%{q}%"),
        )
    )

    if lifecycle:
        systems_query = systems_query.where(StellarSystem.lifecycle == lifecycle)
    if knowledge_layer:
        systems_query = systems_query.where(StellarSystem.knowledge_layer == knowledge_layer)

    systems_result = await db.execute(systems_query)
    systems = systems_result.scalars().all()

    # 搜索星云
    nebulae_query = select(Nebula).where(
        or_(
            Nebula.name.ilike(f"%{q}%"),
            Nebula.content.ilike(f"%{q}%"),
        )
    )
    nebulae_result = await db.execute(nebulae_query)
    nebulae = nebulae_result.scalars().all()

    return SearchResponse(
        systems=systems,
        nebulae=nebulae,
        total=len(systems) + len(nebulae),
    )


# 关系 API
@router.post("/relations", response_model=SystemRelationResponse)
async def create_relation(
    relation: SystemRelationCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建恒星系统间关系"""
    db_relation = SystemRelation(**relation.model_dump())
    db.add(db_relation)
    await db.commit()
    return db_relation


@router.get("/relations", response_model=List[SystemRelationResponse])
async def list_relations(
    db: AsyncSession = Depends(get_db),
):
    """列出所有恒星系统间关系"""
    result = await db.execute(select(SystemRelation))
    relations = result.scalars().all()
    return relations


@router.delete("/relations/{from_system}/{to_system}")
async def delete_relation(
    from_system: str,
    to_system: str,
    db: AsyncSession = Depends(get_db),
):
    """删除恒星系统间关系"""
    result = await db.execute(
        select(SystemRelation).where(
            SystemRelation.from_system == from_system,
            SystemRelation.to_system == to_system,
        )
    )
    relation = result.scalar_one_or_none()

    if relation:
        await db.delete(relation)
        await db.commit()

    return {"message": "关系已删除"}


# 宇宙网纤维 API
@router.post("/fibers", response_model=CosmicWebFiberResponse)
async def create_fiber(
    fiber: CosmicWebFiberCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建宇宙网纤维"""
    db_fiber = CosmicWebFiber(**fiber.model_dump())
    db.add(db_fiber)
    await db.commit()
    await db.refresh(db_fiber)
    return db_fiber


@router.get("/fibers", response_model=List[CosmicWebFiberResponse])
async def list_fibers(
    db: AsyncSession = Depends(get_db),
):
    """列出所有宇宙网纤维"""
    result = await db.execute(select(CosmicWebFiber))
    fibers = result.scalars().all()
    return fibers


@router.delete("/fibers/{fiber_id}")
async def delete_fiber(
    fiber_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除宇宙网纤维"""
    result = await db.execute(
        select(CosmicWebFiber).where(CosmicWebFiber.id == fiber_id)
    )
    fiber = result.scalar_one_or_none()

    if fiber:
        await db.delete(fiber)
        await db.commit()

    return {"message": "宇宙网纤维已删除"}
