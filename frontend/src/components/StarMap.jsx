/**
 * 参星（Trinary）- 星图组件
 * 使用原生 Canvas 渲染知识图谱
 */

import { useEffect, useRef, useState } from 'react'

// 生命周期配置
const LIFECYCLE_CONFIG = {
  protostar: { color: '#FFFFFF', glow: '#FFFFFF', name: '原恒星' },
  main_sequence: { color: '#FFD700', glow: '#FFD700', name: '主序星' },
  red_giant: { color: '#FF4500', glow: '#FF6B6B', name: '红巨星' },
  white_dwarf: { color: '#808080', glow: '#AAAAAA', name: '白矮星' },
  supernova: { color: '#00FFFF', glow: '#00FFFF', name: '超新星' },
}

// 知识层次配置
const KNOWLEDGE_LAYER_CONFIG = {
  fact: { color: '#4A9EFF', shape: 'circle', name: '事实' },
  decision: { color: '#FF6B6B', shape: 'square', name: '决策' },
  insight: { color: '#50C878', shape: 'diamond', name: '洞察' },
  constraint: { color: '#FFD700', shape: 'hexagon', name: '约束' },
}

function StarMap({ systems, clusters, relations, fibers, onSystemClick }) {
  const canvasRef = useRef(null)
  const [hoveredNode, setHoveredNode] = useState(null)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const nodesRef = useRef([])
  const offsetRef = useRef({ x: 0, y: 0 })
  const scaleRef = useRef(1)
  const isDraggingRef = useRef(false)
  const dragStartRef = useRef({ x: 0, y: 0 })
  const animFrameRef = useRef(null)

  useEffect(() => {
    if (systems && systems.length > 0) {
      calculatePositions()
      startAnimation()
    }
    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current)
      }
    }
  }, [systems, clusters, relations])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleWheel = (e) => {
      e.preventDefault()
      const scaleFactor = e.deltaY > 0 ? 0.95 : 1.05
      scaleRef.current = Math.max(0.3, Math.min(3, scaleRef.current * scaleFactor))
      draw()
    }

    const handleMouseDown = (e) => {
      isDraggingRef.current = true
      dragStartRef.current = { x: e.clientX, y: e.clientY }
    }

    const handleMouseMove = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY })

      if (isDraggingRef.current) {
        const dx = e.clientX - dragStartRef.current.x
        const dy = e.clientY - dragStartRef.current.y
        offsetRef.current.x += dx
        offsetRef.current.y += dy
        dragStartRef.current = { x: e.clientX, y: e.clientY }
        draw()
      }

      // 检查悬停
      const rect = canvas.getBoundingClientRect()
      const x = (e.clientX - rect.left - offsetRef.current.x) / scaleRef.current
      const y = (e.clientY - rect.top - offsetRef.current.y) / scaleRef.current

      let found = null
      for (const node of nodesRef.current) {
        const dist = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2)
        if (dist < node.radius + 10) {
          found = node
          break
        }
      }
      setHoveredNode(found)
      canvas.style.cursor = found ? 'pointer' : (isDraggingRef.current ? 'grabbing' : 'grab')
    }

    const handleMouseUp = () => {
      isDraggingRef.current = false
    }

    const handleClick = (e) => {
      if (isDraggingRef.current) return

      const rect = canvas.getBoundingClientRect()
      const x = (e.clientX - rect.left - offsetRef.current.x) / scaleRef.current
      const y = (e.clientY - rect.top - offsetRef.current.y) / scaleRef.current

      for (const node of nodesRef.current) {
        const dist = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2)
        if (dist < node.radius + 10) {
          if (onSystemClick) {
            onSystemClick(node.system.id)
          }
          break
        }
      }
    }

    canvas.addEventListener('wheel', handleWheel, { passive: false })
    canvas.addEventListener('mousedown', handleMouseDown)
    canvas.addEventListener('mousemove', handleMouseMove)
    canvas.addEventListener('mouseup', handleMouseUp)
    canvas.addEventListener('click', handleClick)

    return () => {
      canvas.removeEventListener('wheel', handleWheel)
      canvas.removeEventListener('mousedown', handleMouseDown)
      canvas.removeEventListener('mousemove', handleMouseMove)
      canvas.removeEventListener('mouseup', handleMouseUp)
      canvas.removeEventListener('click', handleClick)
    }
  }, [onSystemClick])

  // 计算节点位置
  const calculatePositions = () => {
    if (!systems) return

    const canvas = canvasRef.current
    if (!canvas) return

    const centerX = canvas.width / 2
    const centerY = canvas.height / 2
    const radius = Math.min(centerX, centerY) * 0.5

    nodesRef.current = systems.map((system, index) => {
      const angle = (index / systems.length) * Math.PI * 2 - Math.PI / 2
      const mass = system.mass || 0.5
      const r = radius * (0.4 + mass * 0.6)
      return {
        x: centerX + Math.cos(angle) * r,
        y: centerY + Math.sin(angle) * r,
        radius: 15 + mass * 35,
        system,
        pulsePhase: Math.random() * Math.PI * 2,
      }
    })

    offsetRef.current = { x: 0, y: 0 }
    scaleRef.current = 1
  }

  // 动画循环
  const startAnimation = () => {
    const animate = () => {
      draw()
      animFrameRef.current = requestAnimationFrame(animate)
    }
    animate()
  }

  // 绘制星图
  const draw = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height
    const time = Date.now() / 1000

    // 清空画布
    ctx.fillStyle = '#050510'
    ctx.fillRect(0, 0, width, height)

    // 绘制背景星星
    drawBackgroundStars(ctx, width, height, time)

    // 保存状态
    ctx.save()

    // 应用变换
    ctx.translate(offsetRef.current.x, offsetRef.current.y)
    ctx.scale(scaleRef.current, scaleRef.current)

    // 绘制星团背景
    if (clusters) {
      drawClusters(ctx, clusters, time)
    }

    // 绘制关系连线
    if (relations) {
      drawRelations(ctx, relations, time)
    }

    // 绘制恒星系统节点
    drawNodes(ctx, time)

    // 恢复状态
    ctx.restore()
  }

  // 绘制背景星星
  const drawBackgroundStars = (ctx, width, height, time) => {
    const starCount = 200
    for (let i = 0; i < starCount; i++) {
      const x = (Math.sin(i * 123.456) * 0.5 + 0.5) * width
      const y = (Math.cos(i * 789.012) * 0.5 + 0.5) * height
      const size = (Math.sin(i * 345.678 + time) * 0.5 + 0.5) * 2 + 0.5
      const alpha = (Math.sin(i * 456.789 + time * 2) * 0.3 + 0.7)

      ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`
      ctx.beginPath()
      ctx.arc(x, y, size, 0, Math.PI * 2)
      ctx.fill()
    }
  }

  // 绘制星团
  const drawClusters = (ctx, clusters, time) => {
    clusters.forEach((cluster) => {
      if (!cluster.systems || cluster.systems.length === 0) return

      let centerX = 0
      let centerY = 0
      let count = 0

      cluster.systems.forEach((sys) => {
        const node = nodesRef.current.find((n) => n.system.id === sys.id)
        if (node) {
          centerX += node.x
          centerY += node.y
          count++
        }
      })

      if (count === 0) return

      centerX /= count
      centerY /= count

      const radius = 100 + count * 30
      const isGlobular = cluster.type === 'globular'

      // 绘制星团光晕
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius)
      if (isGlobular) {
        gradient.addColorStop(0, 'rgba(255, 50, 50, 0.12)')
        gradient.addColorStop(0.5, 'rgba(255, 50, 50, 0.05)')
        gradient.addColorStop(1, 'rgba(255, 50, 50, 0)')
      } else {
        gradient.addColorStop(0, 'rgba(50, 100, 255, 0.12)')
        gradient.addColorStop(0.5, 'rgba(50, 100, 255, 0.05)')
        gradient.addColorStop(1, 'rgba(50, 100, 255, 0)')
      }

      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2)
      ctx.fill()

      // 绘制星团名称
      ctx.fillStyle = isGlobular ? 'rgba(255, 100, 100, 0.7)' : 'rgba(100, 150, 255, 0.7)'
      ctx.font = 'bold 14px Arial'
      ctx.textAlign = 'center'
      ctx.fillText(cluster.name, centerX, centerY - radius - 15)
    })
  }

  // 绘制关系连线
  const drawRelations = (ctx, relations, time) => {
    relations.forEach((relation) => {
      const fromNode = nodesRef.current.find((n) => n.system.id === relation.from_system)
      const toNode = nodesRef.current.find((n) => n.system.id === relation.to_system)

      if (fromNode && toNode) {
        const alpha = 0.2 + Math.sin(time * 2) * 0.1
        ctx.strokeStyle = `rgba(100, 150, 255, ${alpha})`
        ctx.lineWidth = 1 + (relation.strength || 0.5) * 2
        ctx.setLineDash([5, 5])
        ctx.beginPath()
        ctx.moveTo(fromNode.x, fromNode.y)
        ctx.lineTo(toNode.x, toNode.y)
        ctx.stroke()
        ctx.setLineDash([])
      }
    })
  }

  // 绘制节点
  const drawNodes = (ctx, time) => {
    nodesRef.current.forEach((node) => {
      const { x, y, radius, system, pulsePhase } = node
      const lifecycle = LIFECYCLE_CONFIG[system.lifecycle] || LIFECYCLE_CONFIG.protostar
      const layer = KNOWLEDGE_LAYER_CONFIG[system.knowledge_layer] || KNOWLEDGE_LAYER_CONFIG.fact
      const brightness = system.brightness || 0.5
      const isHovered = hoveredNode === node

      // 脉冲动画
      const pulse = Math.sin(time * 2 + pulsePhase) * 0.1 + 1
      const currentRadius = radius * pulse * (isHovered ? 1.2 : 1)

      // 绘制外层光晕
      const outerGlow = ctx.createRadialGradient(x, y, currentRadius * 0.5, x, y, currentRadius * 3)
      outerGlow.addColorStop(0, lifecycle.color + '40')
      outerGlow.addColorStop(0.5, lifecycle.color + '15')
      outerGlow.addColorStop(1, lifecycle.color + '00')
      ctx.fillStyle = outerGlow
      ctx.beginPath()
      ctx.arc(x, y, currentRadius * 3, 0, Math.PI * 2)
      ctx.fill()

      // 绘制内层光晕
      const innerGlow = ctx.createRadialGradient(x, y, 0, x, y, currentRadius * 1.5)
      innerGlow.addColorStop(0, lifecycle.color + '80')
      innerGlow.addColorStop(0.7, lifecycle.color + '30')
      innerGlow.addColorStop(1, lifecycle.color + '00')
      ctx.fillStyle = innerGlow
      ctx.beginPath()
      ctx.arc(x, y, currentRadius * 1.5, 0, Math.PI * 2)
      ctx.fill()

      // 根据知识层次绘制不同形状
      ctx.fillStyle = lifecycle.color
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = isHovered ? 3 : 1.5

      drawShape(ctx, x, y, currentRadius, layer.shape, time, pulsePhase)

      // 绘制高光
      const highlight = ctx.createRadialGradient(x - currentRadius * 0.3, y - currentRadius * 0.3, 0, x, y, currentRadius)
      highlight.addColorStop(0, 'rgba(255, 255, 255, 0.4)')
      highlight.addColorStop(0.5, 'rgba(255, 255, 255, 0.1)')
      highlight.addColorStop(1, 'rgba(255, 255, 255, 0)')
      ctx.fillStyle = highlight
      ctx.beginPath()
      ctx.arc(x, y, currentRadius, 0, Math.PI * 2)
      ctx.fill()

      // 绘制名称
      ctx.fillStyle = '#ffffff'
      ctx.font = `${isHovered ? 'bold ' : ''}12px Arial`
      ctx.textAlign = 'center'
      ctx.shadowColor = 'rgba(0, 0, 0, 0.8)'
      ctx.shadowBlur = 4
      ctx.fillText(system.name, x, y + currentRadius + 18)
      ctx.shadowBlur = 0

      // 绘制生命周期标签
      ctx.fillStyle = lifecycle.color
      ctx.font = '10px Arial'
      ctx.fillText(lifecycle.name, x, y + currentRadius + 32)
    })
  }

  // 绘制形状
  const drawShape = (ctx, x, y, radius, shape, time, phase) => {
    ctx.beginPath()

    switch (shape) {
      case 'circle':
        ctx.arc(x, y, radius, 0, Math.PI * 2)
        break

      case 'square': {
        const size = radius * 1.5
        const angle = Math.sin(time + phase) * 0.1
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(angle)
        ctx.rect(-size / 2, -size / 2, size, size)
        ctx.restore()
        break
      }

      case 'diamond': {
        const size = radius * 1.8
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(Math.PI / 4)
        ctx.rect(-size / 2, -size / 2, size, size)
        ctx.restore()
        break
      }

      case 'hexagon': {
        const sides = 6
        const angle = (Math.PI * 2) / sides
        for (let i = 0; i < sides; i++) {
          const px = x + Math.cos(angle * i - Math.PI / 2) * radius * 1.3
          const py = y + Math.sin(angle * i - Math.PI / 2) * radius * 1.3
          if (i === 0) {
            ctx.moveTo(px, py)
          } else {
            ctx.lineTo(px, py)
          }
        }
        ctx.closePath()
        break
      }

      default:
        ctx.arc(x, y, radius, 0, Math.PI * 2)
    }

    ctx.fill()
    ctx.stroke()
  }

  // 调整画布大小
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const resize = () => {
      canvas.width = canvas.parentElement.clientWidth
      canvas.height = canvas.parentElement.clientHeight
      if (systems && systems.length > 0) {
        calculatePositions()
      }
    }

    resize()
    window.addEventListener('resize', resize)

    return () => {
      window.removeEventListener('resize', resize)
    }
  }, [systems])

  return (
    <div className="star-map" style={{ position: 'relative', width: '100%', height: '100%' }}>
      <canvas
        ref={canvasRef}
        style={{ width: '100%', height: '100%' }}
      />

      {hoveredNode && (
        <div
          className="star-map-tooltip"
          style={{
            position: 'fixed',
            left: mousePos.x + 20,
            top: mousePos.y - 80,
            background: 'linear-gradient(135deg, rgba(20, 20, 40, 0.95), rgba(10, 10, 30, 0.95))',
            border: `1px solid ${LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.color || '#FFD700'}40`,
            borderRadius: '12px',
            padding: '16px',
            pointerEvents: 'none',
            zIndex: 1000,
            minWidth: '220px',
            maxWidth: '300px',
            backdropFilter: 'blur(10px)',
            boxShadow: `0 0 20px ${LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.color || '#FFD700'}20`,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontSize: '20px' }}>
              {KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.name === '决策' ? '■' :
               KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.name === '洞察' ? '▲' :
               KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.name === '约束' ? '◇' : '●'}
            </span>
            <h4 style={{
              margin: 0,
              color: LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.color || '#FFD700',
              fontSize: '14px',
            }}>
              {hoveredNode.system.name}
            </h4>
          </div>
          {hoveredNode.system.star_title && (
            <p style={{ margin: '0 0 8px 0', fontSize: '12px', color: '#aaa' }}>
              {hoveredNode.system.star_title}
            </p>
          )}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <span style={{
              padding: '2px 8px',
              borderRadius: '4px',
              fontSize: '11px',
              background: LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.color + '20',
              color: LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.color,
            }}>
              {LIFECYCLE_CONFIG[hoveredNode.system.lifecycle]?.name}
            </span>
            <span style={{
              padding: '2px 8px',
              borderRadius: '4px',
              fontSize: '11px',
              background: KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.color + '20',
              color: KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.color,
            }}>
              {KNOWLEDGE_LAYER_CONFIG[hoveredNode.system.knowledge_layer]?.name}
            </span>
          </div>
          {hoveredNode.system.planets && hoveredNode.system.planets.length > 0 && (
            <p style={{ margin: '8px 0 0 0', fontSize: '11px', color: '#888' }}>
              📎 {hoveredNode.system.planets.length} 个行星
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default StarMap
