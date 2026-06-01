"""
参星（Trinary）- 知识图谱服务
处理知识提取、分类、关联等业务逻辑
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import StellarSystem, Nebula, SystemHistory


class KnowledgeService:
    """知识图谱服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_knowledge_from_text(
        self,
        text: str,
        source: str = "dialogue",
    ) -> dict:
        """
        从文本中提取知识（简化版）
        实际实现需要调用 AI 模型
        """
        # 这里是简化版本，实际需要调用 MiMo API
        # 返回提取的知识结构
        return {
            "title": text[:50] + "..." if len(text) > 50 else text,
            "summary": text,
            "lifecycle": "protostar",
            "knowledge_layer": "fact",
            "is_knowledge": True,
        }

    async def classify_lifecycle(
        self,
        text: str,
    ) -> str:
        """
        分类生命周期（简化版）
        实际实现需要调用 AI 模型
        """
        # 简化逻辑：根据关键词判断
        if any(word in text for word in ["探索", "尝试", "不确定", "可能"]):
            return "protostar"
        elif any(word in text for word in ["使用", "运行", "活跃"]):
            return "main_sequence"
        elif any(word in text for word in ["沉淀", "总结", "归档"]):
            return "red_giant"
        elif any(word in text for word in ["废弃", "停止"]):
            return "white_dwarf"
        elif any(word in text for word in ["洞察", "教训", "失败"]):
            return "supernova"
        else:
            return "protostar"

    async def classify_knowledge_layer(
        self,
        text: str,
    ) -> str:
        """
        分类知识层次（简化版）
        实际实现需要调用 AI 模型
        """
        # 简化逻辑：根据关键词判断
        if any(word in text for word in ["数据", "信息", "事实", "配置"]):
            return "fact"
        elif any(word in text for word in ["决定", "选择", "方案", "采用"]):
            return "decision"
        elif any(word in text for word in ["洞察", "规律", "原则", "方法论"]):
            return "insight"
        elif any(word in text for word in ["约束", "规则", "必须", "不能"]):
            return "constraint"
        else:
            return "fact"

    async def find_related_systems(
        self,
        text: str,
        limit: int = 5,
    ) -> List[StellarSystem]:
        """
        查找相关的恒星系统（简化版）
        实际实现需要语义相似度计算
        """
        # 简化逻辑：根据关键词匹配
        keywords = text.split()[:5]  # 取前5个词作为关键词

        if not keywords:
            return []

        conditions = []
        for keyword in keywords:
            conditions.append(StellarSystem.name.ilike(f"%{keyword}%"))
            conditions.append(StellarSystem.star_title.ilike(f"%{keyword}%"))
            conditions.append(StellarSystem.star_content.ilike(f"%{keyword}%"))

        query = select(StellarSystem).where(*conditions).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_nebula_from_text(
        self,
        text: str,
        source: str = "dialogue",
        name: Optional[str] = None,
    ) -> Nebula:
        """从文本创建星云"""
        nebula = Nebula(
            name=name,
            content=text,
            source=source,
            density=0.1,
        )
        self.db.add(nebula)
        await self.db.commit()
        await self.db.refresh(nebula)
        return nebula

    async def create_system_from_text(
        self,
        text: str,
        title: Optional[str] = None,
        lifecycle: Optional[str] = None,
        knowledge_layer: Optional[str] = None,
    ) -> StellarSystem:
        """从文本创建恒星系统"""
        # 提取知识
        knowledge = await self.extract_knowledge_from_text(text)

        # 分类
        if not lifecycle:
            lifecycle = await self.classify_lifecycle(text)
        if not knowledge_layer:
            knowledge_layer = await self.classify_knowledge_layer(text)

        # 创建恒星系统
        system = StellarSystem(
            name=title or knowledge["title"],
            star_title=title or knowledge["title"],
            star_summary=knowledge["summary"],
            star_content=text,
            lifecycle=lifecycle,
            knowledge_layer=knowledge_layer,
            brightness=0.5,
            mass=0.5,
        )
        self.db.add(system)

        # 添加历史记录
        history = SystemHistory(
            system_id=system.id,
            event="原恒星诞生",
            detail="从文本中提取创建",
        )
        self.db.add(history)

        await self.db.commit()
        await self.db.refresh(system)
        return system
