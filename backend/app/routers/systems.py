"""
参星（Trinary）- 恒星系统 API
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import StellarSystem, Planet, Satellite, SystemHistory
from ..schemas import (
    StellarSystemCreate,
    StellarSystemUpdate,
    StellarSystemResponse,
    PlanetCreate,
    PlanetResponse,
    SatelliteCreate,
    SatelliteResponse,
    HistoryResponse,
)

router = APIRouter()


@router.get("/", response_model=List[StellarSystemResponse])
async def list_systems(
    lifecycle: Optional[str] = Query(None, description="生命周期筛选"),
    knowledge_layer: Optional[str] = Query(None, description="知识层次筛选"),
    db: AsyncSession = Depends(get_db),
):
    """列出所有恒星系统"""
    query = select(StellarSystem).options(
        selectinload(StellarSystem.planets).selectinload(Planet.satellites)
    )

    if lifecycle:
        query = query.where(StellarSystem.lifecycle == lifecycle)
    if knowledge_layer:
        query = query.where(StellarSystem.knowledge_layer == knowledge_layer)

    result = await db.execute(query)
    systems = result.scalars().unique().all()
    return systems


@router.post("/", response_model=StellarSystemResponse)
async def create_system(
    system: StellarSystemCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建恒星系统"""
    db_system = StellarSystem(**system.model_dump())
    db.add(db_system)

    # 添加历史记录
    history = SystemHistory(
        system_id=db_system.id,
        event="原恒星诞生",
        detail="从创建请求中生成",
    )
    db.add(history)

    await db.commit()
    await db.refresh(db_system)
    return db_system


@router.get("/{system_id}", response_model=StellarSystemResponse)
async def get_system(
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取恒星系统详情"""
    result = await db.execute(
        select(StellarSystem)
        .options(
            selectinload(StellarSystem.planets).selectinload(Planet.satellites)
        )
        .where(StellarSystem.id == system_id)
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="恒星系统不存在")

    return system


@router.put("/{system_id}", response_model=StellarSystemResponse)
async def update_system(
    system_id: str,
    system_update: StellarSystemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新恒星系统"""
    result = await db.execute(
        select(StellarSystem).where(StellarSystem.id == system_id)
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="恒星系统不存在")

    # 更新字段
    update_data = system_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(system, field, value)

    # 添加历史记录
    history = SystemHistory(
        system_id=system_id,
        event="更新",
        detail=f"更新了字段: {', '.join(update_data.keys())}",
    )
    db.add(history)

    await db.commit()
    await db.refresh(system)
    return system


@router.delete("/{system_id}")
async def delete_system(
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除恒星系统"""
    result = await db.execute(
        select(StellarSystem).where(StellarSystem.id == system_id)
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="恒星系统不存在")

    await db.delete(system)
    await db.commit()

    return {"message": "恒星系统已删除"}


@router.get("/{system_id}/history", response_model=List[HistoryResponse])
async def get_system_history(
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取恒星系统历史记录"""
    result = await db.execute(
        select(SystemHistory)
        .where(SystemHistory.system_id == system_id)
        .order_by(SystemHistory.timestamp.desc())
    )
    history = result.scalars().all()
    return history


# 行星 API
@router.post("/{system_id}/planets", response_model=PlanetResponse)
async def create_planet(
    system_id: str,
    planet: PlanetCreate,
    db: AsyncSession = Depends(get_db),
):
    """为恒星系统创建行星"""
    # 检查恒星系统是否存在
    result = await db.execute(
        select(StellarSystem).where(StellarSystem.id == system_id)
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="恒星系统不存在")

    db_planet = Planet(system_id=system_id, **planet.model_dump())
    db.add(db_planet)

    # 添加历史记录
    history = SystemHistory(
        system_id=system_id,
        event="行星形成",
        detail=f"新增行星: {planet.title}",
    )
    db.add(history)

    await db.commit()
    await db.refresh(db_planet)
    return db_planet


@router.get("/{system_id}/planets", response_model=List[PlanetResponse])
async def list_planets(
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """列出恒星系统的所有行星"""
    result = await db.execute(
        select(Planet).where(Planet.system_id == system_id)
    )
    planets = result.scalars().all()
    return planets


# 卫星 API
@router.post("/planets/{planet_id}/satellites", response_model=SatelliteResponse)
async def create_satellite(
    planet_id: str,
    satellite: SatelliteCreate,
    db: AsyncSession = Depends(get_db),
):
    """为行星创建卫星"""
    # 检查行星是否存在
    result = await db.execute(
        select(Planet).where(Planet.id == planet_id)
    )
    planet = result.scalar_one_or_none()

    if not planet:
        raise HTTPException(status_code=404, detail="行星不存在")

    db_satellite = Satellite(planet_id=planet_id, **satellite.model_dump())
    db.add(db_satellite)
    await db.commit()
    await db.refresh(db_satellite)
    return db_satellite


@router.get("/planets/{planet_id}/satellites", response_model=List[SatelliteResponse])
async def list_satellites(
    planet_id: str,
    db: AsyncSession = Depends(get_db),
):
    """列出行星的所有卫星"""
    result = await db.execute(
        select(Satellite).where(Satellite.planet_id == planet_id)
    )
    satellites = result.scalars().all()
    return satellites
