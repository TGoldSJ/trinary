/**
 * 参星（Trinary）- 详情面板组件
 */

import { useState, useEffect } from 'react'
import api from '../services/api'

const LIFECYCLE_CONFIG = {
  protostar: { name: '原恒星', color: '#FFFFFF' },
  main_sequence: { name: '主序星', color: '#FFD700' },
  red_giant: { name: '红巨星', color: '#FF4500' },
  white_dwarf: { name: '白矮星', color: '#808080' },
  supernova: { name: '超新星', color: '#00FFFF' },
}

const KNOWLEDGE_LAYER_CONFIG = {
  fact: { name: '事实', color: '#4A9EFF' },
  decision: { name: '决策', color: '#FF6B6B' },
  insight: { name: '洞察', color: '#50C878' },
  constraint: { name: '约束', color: '#FFD700' },
}

function DetailPanel({ system, onClose, onUpdate }) {
  const [history, setHistory] = useState([])
  const [planets, setPlanets] = useState([])
  const [loading, setLoading] = useState(false)
  const [editMode, setEditMode] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    star_title: '',
    star_summary: '',
    star_content: '',
    lifecycle: '',
    knowledge_layer: '',
  })

  useEffect(() => {
    if (system) {
      setFormData({
        name: system.name || '',
        star_title: system.star_title || '',
        star_summary: system.star_summary || '',
        star_content: system.star_content || '',
        lifecycle: system.lifecycle || '',
        knowledge_layer: system.knowledge_layer || '',
      })
      loadHistory()
      loadPlanets()
    }
  }, [system])

  const loadHistory = async () => {
    try {
      const data = await api.getSystemHistory(system.id)
      setHistory(data)
    } catch (err) {
      console.error('加载历史记录失败:', err)
    }
  }

  const loadPlanets = async () => {
    try {
      const data = await api.getPlanets(system.id)
      setPlanets(data)
    } catch (err) {
      console.error('加载行星失败:', err)
    }
  }

  const handleSave = async () => {
    try {
      setLoading(true)
      await api.updateSystem(system.id, formData)
      setEditMode(false)
      if (onUpdate) onUpdate()
    } catch (err) {
      console.error('更新失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('确定要删除这个恒星系统吗？')) return
    try {
      setLoading(true)
      await api.deleteSystem(system.id)
      if (onUpdate) onUpdate()
      onClose()
    } catch (err) {
      console.error('删除失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  if (!system) return null

  const lifecycle = LIFECYCLE_CONFIG[system.lifecycle] || LIFECYCLE_CONFIG.protostar
  const layer = KNOWLEDGE_LAYER_CONFIG[system.knowledge_layer] || KNOWLEDGE_LAYER_CONFIG.fact

  return (
    <div className="detail-panel">
      <div className="detail-panel-header">
        <h2 style={{ color: lifecycle.color }}>{system.name}</h2>
        <button className="close-button" onClick={onClose}>✕</button>
      </div>

      <div className="detail-panel-content">
        {editMode ? (
          <div className="edit-form">
            <div className="form-group">
              <label>名称</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>标题</label>
              <input type="text" name="star_title" value={formData.star_title} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>摘要</label>
              <textarea name="star_summary" value={formData.star_summary} onChange={handleChange} rows={3} />
            </div>
            <div className="form-group">
              <label>内容</label>
              <textarea name="star_content" value={formData.star_content} onChange={handleChange} rows={5} />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>生命周期</label>
                <select name="lifecycle" value={formData.lifecycle} onChange={handleChange}>
                  {Object.entries(LIFECYCLE_CONFIG).map(([key, config]) => (
                    <option key={key} value={key}>{config.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>知识层次</label>
                <select name="knowledge_layer" value={formData.knowledge_layer} onChange={handleChange}>
                  {Object.entries(KNOWLEDGE_LAYER_CONFIG).map(([key, config]) => (
                    <option key={key} value={key}>{config.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="form-actions">
              <button onClick={handleSave} disabled={loading}>
                {loading ? '保存中...' : '保存'}
              </button>
              <button onClick={() => setEditMode(false)}>取消</button>
            </div>
          </div>
        ) : (
          <div className="view-mode">
            <div className="info-section">
              <h3>基本信息</h3>
              <p><strong>生命周期:</strong> <span style={{ color: lifecycle.color }}>{lifecycle.name}</span></p>
              <p><strong>知识层次:</strong> <span style={{ color: layer.color }}>{layer.name}</span></p>
              <p><strong>亮度:</strong> {Math.round((system.brightness || 0) * 100)}%</p>
              <p><strong>质量:</strong> {Math.round((system.mass || 0) * 100)}%</p>
            </div>

            {system.star_summary && (
              <div className="info-section">
                <h3>摘要</h3>
                <p>{system.star_summary}</p>
              </div>
            )}

            {system.star_content && (
              <div className="info-section">
                <h3>内容</h3>
                <p style={{ whiteSpace: 'pre-wrap' }}>{system.star_content}</p>
              </div>
            )}

            {planets.length > 0 && (
              <div className="info-section">
                <h3>行星（派生知识）</h3>
                <ul className="planets-list">
                  {planets.map((planet) => (
                    <li key={planet.id}>
                      <strong>{planet.title}</strong>
                      {planet.summary && <p>{planet.summary}</p>}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {history.length > 0 && (
              <div className="info-section">
                <h3>历史记录</h3>
                <ul className="history-list">
                  {history.map((item) => (
                    <li key={item.id}>
                      <span className="history-time">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                      <span className="history-event">{item.event}</span>
                      {item.detail && <span className="history-detail">{item.detail}</span>}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="info-section">
              <h3>时间信息</h3>
              <p><strong>创建时间:</strong> {new Date(system.created_at).toLocaleString()}</p>
              <p><strong>更新时间:</strong> {new Date(system.updated_at).toLocaleString()}</p>
            </div>
          </div>
        )}
      </div>

      <div className="detail-panel-footer">
        {!editMode && (
          <>
            <button onClick={() => setEditMode(true)}>编辑</button>
            <button className="delete-button" onClick={handleDelete}>删除</button>
          </>
        )}
      </div>
    </div>
  )
}

export default DetailPanel
