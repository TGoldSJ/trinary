import { useState, useEffect } from 'react'
import StarMap from './components/StarMap'
import Sidebar from './components/Sidebar'
import DetailPanel from './components/DetailPanel'
import api from './services/api'

function App() {
  const [galaxy, setGalaxy] = useState(null)
  const [selectedSystem, setSelectedSystem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    loadGalaxy()
  }, [])

  const loadGalaxy = async () => {
    try {
      setLoading(true)
      const data = await api.getGalaxy()
      setGalaxy(data)
      setError(null)
    } catch (err) {
      console.error('加载星系数据失败:', err)
      setError('加载星系数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleSystemClick = async (systemId) => {
    try {
      const system = await api.getSystem(systemId)
      setSelectedSystem(system)
    } catch (err) {
      console.error('获取详情失败:', err)
    }
  }

  const handleCloseDetail = () => {
    setSelectedSystem(null)
  }

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>正在加载星系数据...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app-error">
        <h2>错误</h2>
        <p>{error}</p>
        <button onClick={loadGalaxy}>重试</button>
      </div>
    )
  }

  return (
    <div className="app">
      {/* 顶部导航 */}
      <header className="app-header">
        <button
          className="menu-btn"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? '✕' : '☰'}
        </button>
        <div className="logo">
          <span className="logo-icon">✦</span>
          <h1>参星</h1>
          <span className="logo-sub">Trinary</span>
        </div>
        <div className="header-stats">
          {galaxy && (
            <>
              <span className="stat">
                <span className="stat-icon">⭐</span>
                <span className="stat-value">{galaxy.systems?.length || 0}</span>
                <span className="stat-label">恒星</span>
              </span>
              <span className="stat">
                <span className="stat-icon">☁️</span>
                <span className="stat-value">{galaxy.nebulae?.length || 0}</span>
                <span className="stat-label">星云</span>
              </span>
              <span className="stat">
                <span className="stat-icon">🌌</span>
                <span className="stat-value">{galaxy.clusters?.length || 0}</span>
                <span className="stat-label">星团</span>
              </span>
            </>
          )}
        </div>
      </header>

      <div className="app-body">
        {/* 侧边栏 */}
        <Sidebar
          galaxy={galaxy}
          isOpen={sidebarOpen}
          onSystemClick={handleSystemClick}
          selectedSystemId={selectedSystem?.id}
        />

        {/* 主内容区 */}
        <main className="app-main">
          <div className="star-map-container">
            {galaxy && (
              <StarMap
                systems={galaxy.systems}
                clusters={galaxy.clusters}
                relations={galaxy.relations}
                fibers={galaxy.fibers}
                onSystemClick={handleSystemClick}
              />
            )}
          </div>

          {/* 详情面板 */}
          {selectedSystem && (
            <DetailPanel
              system={selectedSystem}
              onClose={handleCloseDetail}
              onUpdate={loadGalaxy}
            />
          )}
        </main>
      </div>
    </div>
  )
}

export default App
