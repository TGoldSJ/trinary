"""
参星（Trinary）- 基于天文隐喻的知识图谱系统
FastAPI 后端入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import init_db
from .routers import systems, nebulae, clusters, galaxy


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源


app = FastAPI(
    title="参星（Trinary）",
    description="基于天文隐喻的知识图谱系统",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(systems.router, prefix="/api/systems", tags=["恒星系统"])
app.include_router(nebulae.router, prefix="/api/nebulae", tags=["星云"])
app.include_router(clusters.router, prefix="/api/clusters", tags=["星团"])
app.include_router(galaxy.router, prefix="/api/galaxy", tags=["星系"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "参星（Trinary）",
        "description": "基于天文隐喻的知识图谱系统",
        "version": "0.1.0",
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
