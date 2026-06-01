"""
参星（Trinary）- 星云 API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import Nebula, StellarSystem, SystemHistory
from ..schemas import NebulaCreate, NebulaResponse, StellarSystemResponse

router = APIRouter()


@router.get("/", response_model=List[NebulaResponse])
async def list_nebulae(
    db: AsyncSession = Depends(get_db),
):
    """列出所有星云"""
    result = await db.execute(select(Nebula))
    nebulae = result.scalars().all()
    return nebulae


@router.post("/", response_model=NebulaResponse)
async def create_nebula(
    nebula: NebulaCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建星云"""
    db_nebula = Nebula(**nebula.model_dump())
    db.add(db_nebula)
    await db.commit()
    await db.refresh(db_nebula)
    return db_nebula


@router.get("/{nebula_id}", response_model=NebulaResponse)
async def get_nebula(
    nebula_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取星云详情"""
    result = await db.execute(
        select(Nebula).where(Nebula.id == nebula_id)
    )
    nebula = result.scalar_one_or_none()

    if not nebula:
        raise HTTPException(status_code=404, detail="星云不存在")

    return nebula


@router.post("/{nebula_id}/condense", response_model=StellarSystemResponse)
async def condense_nebula(
    nebula_id: str,
    db: AsyncSession = Depends(get_db),
):
    """星云凝聚为恒星"""
    # 获取星云
    result = await db.execute(
        select(Nebula).where(Nebula.id == nebula_id)
    )
    nebula = result.scalar_one_or_none()

    if not nebula:
        raise HTTPException(status_code=404, detail="星云不存在")

    # 创建恒星系统
    system = StellarSystem(
        name=nebula.name or "新凝聚的恒星",
        star_title=nebula.name,
        star_content=nebula.content,
        lifecycle="protostar",
        knowledge_layer="fact",
    )
    db.add(system)

    # 添加历史记录
    history = SystemHistory(
        system_id=system.id,
        event="原恒星诞生",
        detail=f"从星云 {nebula_id} 凝聚而成",
    )
    db.add(history)

    # 更新星云状态
    nebula.absorbed_by = system.id

    await db.commit()
    await db.refresh(system)

    return system


@router.delete("/{nebula_id}")
async def delete_nebula(
    nebula_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除星云"""
    result = await db.execute(
        select(Nebula).where(Nebula.id == nebula_id)
    )
    nebula = result.scalar_one_or_none()

    if not nebula:
        raise HTTPException(status_code=404, detail="星云不存在")

    await db.delete(nebula)
    await db.commit()

    return {"message": "星云已删除"}
