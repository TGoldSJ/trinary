"""
参星（Trinary）- 种子数据
创建初始示例数据
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from app.database import init_db, async_session
from app.models import StellarSystem, Nebula, Cluster, Planet, SystemHistory, SystemClusterMap


async def seed_data():
    """创建种子数据"""
    # 初始化数据库
    await init_db()

    async with async_session() as session:
        # 检查是否已有数据
        from sqlalchemy import select, func
        result = await session.execute(select(func.count(StellarSystem.id)))
        count = result.scalar()

        if count > 0:
            print(f"数据库已有 {count} 个恒星系统，跳过种子数据创建")
            return

        print("创建种子数据...")

        # 1. 创建参星恒星系统
        trinary = StellarSystem(
            name="参星（Trinary）",
            star_title="基于天文隐喻的知识图谱系统",
            star_summary="用星云、恒星、星团、旋臂、宇宙网等天文结构来组织知识，让知识的组织方式本身成为知识的一部分。",
            star_content="""参星的核心理念：

1. 知识决定输出质量 - AI 执行的正确性完全取决于它拥有的知识质量
2. 人类识别模式，AI 执行模式 - 人类发现规律，AI 遵循规则
3. 失败编码为规则 - 每次失败 = 1 条新规则

天文隐喻体系：
- 星云：知识原料池（原始想法、灵感碎片）
- 恒星：知识单元（已凝聚的知识点）
- 行星：派生知识（从核心知识延伸）
- 星团：知识聚类（多个恒星系统的聚合）
- 旋臂：知识密度路径（由关联密度自动涌现）
- 超新星：洞察爆发（项目结束后散落的高价值洞察）

两个正交维度：
- 生命周期：原恒星 → 主序星 → 红巨星 → 白矮星 / 超新星
- 知识层次：事实 / 决策 / 洞察 / 约束""",
            lifecycle="main_sequence",
            knowledge_layer="decision",
            brightness=0.9,
            mass=0.95,
        )
        session.add(trinary)
        await session.flush()

        # 添加历史记录
        history1 = SystemHistory(
            system_id=trinary.id,
            event="原恒星诞生",
            detail="2026-04-28 项目原点讨论",
        )
        history2 = SystemHistory(
            system_id=trinary.id,
            event="进入主序",
            detail="2026-05-25 理论模型 v6 终稿完成",
        )
        history3 = SystemHistory(
            system_id=trinary.id,
            event="融合 Overmind",
            detail="2026-06-01 融合知识驱动开发理念，升级为 v7",
        )
        session.add_all([history1, history2, history3])

        # 2. 创建天文隐喻恒星系统
        astronomy = StellarSystem(
            name="天文隐喻体系",
            star_title="参星的组织语言",
            star_summary="用真实天文结构映射知识图谱概念",
            star_content="星云→恒星→行星→卫星→星团→旋臂→宇宙网",
            lifecycle="main_sequence",
            knowledge_layer="insight",
            brightness=0.8,
            mass=0.8,
        )
        session.add(astronomy)
        await session.flush()

        # 3. 创建 Overmind 理念恒星系统
        overmind = StellarSystem(
            name="Overmind 理念",
            star_title="知识驱动开发宣言",
            star_summary="知识决定输出质量，人类识别模式，AI执行模式",
            star_content="核心理念：知识是任何AI不知道就只能猜测的东西",
            lifecycle="main_sequence",
            knowledge_layer="insight",
            brightness=0.85,
            mass=0.85,
        )
        session.add(overmind)
        await session.flush()

        # 4. 创建知识循环恒星系统
        cycle = StellarSystem(
            name="知识循环机制",
            star_title="双循环系统",
            star_summary="生命周期循环 + 反馈循环",
            star_content="星云→恒星→超新星→星云（生命周期）\n知识→执行→反馈→知识（反馈循环）",
            lifecycle="main_sequence",
            knowledge_layer="decision",
            brightness=0.7,
            mass=0.7,
        )
        session.add(cycle)
        await session.flush()

        # 5. 创建星云示例
        nebula1 = Nebula(
            name="AI 协作灵感",
            content="如果能让 AI 自动从对话中提取知识，并用可视化方式组织...",
            source="dialogue",
            density=0.3,
        )
        nebula2 = Nebula(
            name="失败编码想法",
            content="每次失败都应该编码为规则，系统永远不会以同样方式失败两次",
            source="reflection",
            density=0.5,
        )
        session.add_all([nebula1, nebula2])

        # 6. 创建星团示例
        cluster1 = Cluster(
            name="核心理论",
            type="globular",
            center_system_id=trinary.id,
            density=0.9,
            age="成熟",
            status="active",
        )
        cluster2 = Cluster(
            name="设计理念",
            type="open",
            center_system_id=astronomy.id,
            density=0.6,
            age="年轻",
            status="active",
        )
        session.add_all([cluster1, cluster2])
        await session.flush()

        # 7. 创建行星示例
        planet1 = Planet(
            system_id=trinary.id,
            title="五层结构",
            summary="星云→恒星系统→星团→星系→宇宙网",
        )
        planet2 = Planet(
            system_id=trinary.id,
            title="两个正交维度",
            summary="生命周期（成熟度）× 知识层次（内容性质）",
        )
        planet3 = Planet(
            system_id=trinary.id,
            title="三层过滤机制",
            summary="规则预过滤→意图初筛→深度分析",
        )
        session.add_all([planet1, planet2, planet3])
        await session.flush()

        # 8. 关联恒星系统到星团
        mapping1 = SystemClusterMap(system_id=trinary.id, cluster_id=cluster1.id)
        mapping2 = SystemClusterMap(system_id=astronomy.id, cluster_id=cluster1.id)
        mapping3 = SystemClusterMap(system_id=overmind.id, cluster_id=cluster2.id)
        mapping4 = SystemClusterMap(system_id=cycle.id, cluster_id=cluster1.id)
        session.add_all([mapping1, mapping2, mapping3, mapping4])

        # 提交事务
        await session.commit()

        print("种子数据创建成功！")
        print(f"  - 恒星系统: 4 个")
        print(f"  - 星云: 2 个")
        print(f"  - 星团: 2 个")
        print(f"  - 行星: 3 个")


if __name__ == "__main__":
    asyncio.run(seed_data())
