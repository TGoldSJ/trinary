/**
 * 参星（Trinary）- 侧边栏组件
 */

import { useState } from 'react'

// 生命周期配置
const LIFECYCLE_CONFIG = {
  protostar: { name: '原恒星', color: '#FFFFFF', icon: '✧' },
  main_sequence: { name: '主序星', color: '#FFD700', icon: '★' },
  red_giant: { name: '红巨星', color: '#FF4500', icon: '◉' },
  white_dwarf: { name: '白矮星', color: '#808080', icon: '○' },
  supernova: { name: '超新星', color: '#00FFFF', icon: '✦' },
}

// 知识层次配置
const KNOWLEDGE_LAYER_CONFIG = {
  fact: { name: '事实', color: '#4A9EFF', icon: '◆' },
  decision: { name: '决策', color: '#FF6B6B', icon: '■' },
  insight: { name: '洞察', color: '#50C878', icon: '▲' },
  constraint: { name: '约束', color: '#FFD700', icon: '◇' },
}

function Sidebar({ galaxy, isOpen, onSystemClick, selectedSystemId }) {
  const [activeTab, setActiveTab] = useState('systems')
  const [filterLifecycle, setFilterLifecycle] = useState(null)
  const [filterLayer, setFilterLayer] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  if (!galaxy) return null

  // 过滤系统
  const filteredSystems = (galaxy.systems || []).filter((system) => {
    if (filterLifecycle && system.lifecycle !== filterLifecycle) return false
    if (filterLayer && system.knowledge_layer !== filterLayer) return false
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      return (
        system.name.toLowerCase().includes(query) ||
        system.star_title?.toLowerCase().includes(query) ||
        system.star_summary?.toLowerCase().includes(query)
      )
    }
    return true
  })

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      {/* 标签页 */}
      <div className="sidebar-tabs">
        <button
          className={`tab ${activeTab === 'systems' ? 'active' : ''}`}
          onClick={() => setActiveTab('systems')}
        >
          ⭐ 恒星系统
        </button>
        <button
          className={`tab ${activeTab === 'clusters' ? 'active' : ''}`}
          onClick={() => setActiveTab('clusters')}
        >
          🌌 星团
        </button>
        <button
          className={`tab ${activeTab === 'nebulae' ? 'active' : ''}`}
          onClick={() => setActiveTab('nebulae')}
        >
          ☁️ 星云
        </button>
      </div>

      {/* 搜索框 */}
      <div className="sidebar-search">
        <input
          type="text"
          placeholder="搜索知识..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* 筛选器 */}
      {activeTab === 'systems' && (
        <div className="sidebar-filters">
          <div className="filter-group">
            <label>生命周期</label>
            <div className="filter-options">
              <button
                className={`filter-btn ${!filterLifecycle ? 'active' : ''}`}
                onClick={() => setFilterLifecycle(null)}
              >
                全部
              </button>
              {Object.entries(LIFECYCLE_CONFIG).map(([key, config]) => (
                <button
                  key={key}
                  className={`filter-btn ${filterLifecycle === key ? 'active' : ''}`}
                  onClick={() => setFilterLifecycle(filterLifecycle === key ? null : key)}
                  style={{ '--filter-color': config.color }}
                >
                  {config.icon}
                </button>
              ))}
            </div>
          </div>
          <div className="filter-group">
            <label>知识层次</label>
            <div className="filter-options">
              <button
                className={`filter-btn ${!filterLayer ? 'active' : ''}`}
                onClick={() => setFilterLayer(null)}
              >
                全部
              </button>
              {Object.entries(KNOWLEDGE_LAYER_CONFIG).map(([key, config]) => (
                <button
                  key={key}
                  className={`filter-btn ${filterLayer === key ? 'active' : ''}`}
                  onClick={() => setFilterLayer(filterLayer === key ? null : key)}
                  style={{ '--filter-color': config.color }}
                >
                  {config.icon}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 内容列表 */}
      <div className="sidebar-content">
        {activeTab === 'systems' && (
          <div className="systems-list">
            {filteredSystems.map((system) => {
              const lifecycle = LIFECYCLE_CONFIG[system.lifecycle] || LIFECYCLE_CONFIG.protostar
              const layer = KNOWLEDGE_LAYER_CONFIG[system.knowledge_layer] || KNOWLEDGE_LAYER_CONFIG.fact

              return (
                <div
                  key={system.id}
                  className={`system-card ${selectedSystemId === system.id ? 'selected' : ''}`}
                  onClick={() => onSystemClick(system.id)}
                >
                  <div className="system-card-header">
                    <span
                      className="system-icon"
                      style={{ color: lifecycle.color }}
                    >
                      {lifecycle.icon}
                    </span>
                    <span className="system-name">{system.name}</span>
                  </div>
                  {system.star_title && (
                    <div className="system-title">{system.star_title}</div>
                  )}
                  <div className="system-meta">
                    <span
                      className="meta-tag lifecycle"
                      style={{ color: lifecycle.color }}
                    >
                      {lifecycle.name}
                    </span>
                    <span
                      className="meta-tag layer"
                      style={{ color: layer.color }}
                    >
                      {layer.name}
                    </span>
                  </div>
                  {system.star_summary && (
                    <div className="system-summary">
                      {system.star_summary.substring(0, 60)}...
                    </div>
                  )}
                  {system.planets && system.planets.length > 0 && (
                    <div className="system-planets">
                      📎 {system.planets.length} 个行星
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}

        {activeTab === 'clusters' && (
          <div className="clusters-list">
            {(galaxy.clusters || []).map((cluster) => (
              <div key={cluster.id} className="cluster-card">
                <div className="cluster-card-header">
                  <span className="cluster-icon">
                    {cluster.type === 'globular' ? '🔴' : '🔵'}
                  </span>
                  <span className="cluster-name">{cluster.name}</span>
                </div>
                <div className="cluster-meta">
                  <span>{cluster.type === 'globular' ? '球状星团' : '疏散星团'}</span>
                  <span>•</span>
                  <span>{cluster.systems?.length || 0} 个系统</span>
                </div>
                {cluster.systems && cluster.systems.length > 0 && (
                  <div className="cluster-systems">
                    {cluster.systems.map((sys) => (
                      <span
                        key={sys.id}
                        className="cluster-system-tag"
                        onClick={() => onSystemClick(sys.id)}
                      >
                        {sys.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {activeTab === 'nebulae' && (
          <div className="nebulae-list">
            {(galaxy.nebulae || []).map((nebula) => (
              <div key={nebula.id} className="nebula-card">
                <div className="nebula-card-header">
                  <span className="nebula-icon">☁️</span>
                  <span className="nebula-name">{nebula.name || '未命名星云'}</span>
                </div>
                <div className="nebula-content">
                  {nebula.content?.substring(0, 80)}...
                </div>
                <div className="nebula-meta">
                  <span>密度: {Math.round((nebula.density || 0) * 100)}%</span>
                  <span>•</span>
                  <span>{nebula.source || '未知来源'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </aside>
  )
}

export default Sidebar
