"""
参星（Trinary）- 星团 API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import Cluster, StellarSystem, SystemClusterMap
from ..schemas import ClusterCreate, ClusterResponse, StellarSystemResponse

router = APIRouter()


@router.get("/", response_model=List[ClusterResponse])
async def list_clusters(
    db: AsyncSession = Depends(get_db),
):
    """列出所有星团"""
    result = await db.execute(select(Cluster))
    clusters = result.scalars().all()
    return clusters


@router.post("/", response_model=ClusterResponse)
async def create_cluster(
    cluster: ClusterCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建星团"""
    db_cluster = Cluster(**cluster.model_dump())
    db.add(db_cluster)
    await db.commit()
    await db.refresh(db_cluster)
    return db_cluster


@router.get("/{cluster_id}", response_model=ClusterResponse)
async def get_cluster(
    cluster_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取星团详情"""
    result = await db.execute(
        select(Cluster).where(Cluster.id == cluster_id)
    )
    cluster = result.scalar_one_or_none()

    if not cluster:
        raise HTTPException(status_code=404, detail="星团不存在")

    return cluster


@router.post("/{cluster_id}/systems/{system_id}")
async def add_system_to_cluster(
    cluster_id: str,
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """将恒星系统添加到星团"""
    # 检查星团是否存在
    cluster_result = await db.execute(
        select(Cluster).where(Cluster.id == cluster_id)
    )
    cluster = cluster_result.scalar_one_or_none()

    if not cluster:
        raise HTTPException(status_code=404, detail="星团不存在")

    # 检查恒星系统是否存在
    system_result = await db.execute(
        select(StellarSystem).where(StellarSystem.id == system_id)
    )
    system = system_result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="恒星系统不存在")

    # 检查是否已存在
    existing = await db.execute(
        select(SystemClusterMap).where(
            SystemClusterMap.system_id == system_id,
            SystemClusterMap.cluster_id == cluster_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="恒星系统已在星团中")

    # 添加关联
    mapping = SystemClusterMap(system_id=system_id, cluster_id=cluster_id)
    db.add(mapping)
    await db.commit()

    return {"message": "恒星系统已添加到星团"}


@router.delete("/{cluster_id}/systems/{system_id}")
async def remove_system_from_cluster(
    cluster_id: str,
    system_id: str,
    db: AsyncSession = Depends(get_db),
):
    """从星团中移除恒星系统"""
    result = await db.execute(
        select(SystemClusterMap).where(
            SystemClusterMap.system_id == system_id,
            SystemClusterMap.cluster_id == cluster_id,
        )
    )
    mapping = result.scalar_one_or_none()

    if not mapping:
        raise HTTPException(status_code=404, detail="恒星系统不在星团中")

    await db.delete(mapping)
    await db.commit()

    return {"message": "恒星系统已从星团中移除"}


@router.get("/{cluster_id}/systems", response_model=List[StellarSystemResponse])
async def list_cluster_systems(
    cluster_id: str,
    db: AsyncSession = Depends(get_db),
):
    """列出星团中的所有恒星系统"""
    # 检查星团是否存在
    cluster_result = await db.execute(
        select(Cluster).where(Cluster.id == cluster_id)
    )
    cluster = cluster_result.scalar_one_or_none()

    if not cluster:
        raise HTTPException(status_code=404, detail="星团不存在")

    # 获取星团中的恒星系统
    result = await db.execute(
        select(StellarSystem)
        .join(SystemClusterMap, SystemClusterMap.system_id == StellarSystem.id)
        .where(SystemClusterMap.cluster_id == cluster_id)
    )
    systems = result.scalars().all()

    return systems


@router.delete("/{cluster_id}")
async def delete_cluster(
    cluster_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除星团"""
    result = await db.execute(
        select(Cluster).where(Cluster.id == cluster_id)
    )
    cluster = result.scalar_one_or_none()

    if not cluster:
        raise HTTPException(status_code=404, detail="星团不存在")

    await db.delete(cluster)
    await db.commit()

    return {"message": "星团已删除"}
