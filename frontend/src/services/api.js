/**
 * 参星（Trinary）- API 服务
 * 封装与后端的通信
 */

import axios from 'axios'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API 错误:', error)
    return Promise.reject(error)
  }
)

const api = {
  // 星系 API
  async getGalaxy() {
    return apiClient.get('/galaxy')
  },

  async searchGalaxy(query) {
    return apiClient.get('/galaxy/search', { params: { q: query } })
  },

  // 恒星系统 API
  async getSystems(filters = {}) {
    return apiClient.get('/systems', { params: filters })
  },

  async getSystem(systemId) {
    return apiClient.get(`/systems/${systemId}`)
  },

  async createSystem(systemData) {
    return apiClient.post('/systems', systemData)
  },

  async updateSystem(systemId, systemData) {
    return apiClient.put(`/systems/${systemId}`, systemData)
  },

  async deleteSystem(systemId) {
    return apiClient.delete(`/systems/${systemId}`)
  },

  async getSystemHistory(systemId) {
    return apiClient.get(`/systems/${systemId}/history`)
  },

  // 行星 API
  async createPlanet(systemId, planetData) {
    return apiClient.post(`/systems/${systemId}/planets`, planetData)
  },

  async getPlanets(systemId) {
    return apiClient.get(`/systems/${systemId}/planets`)
  },

  // 卫星 API
  async createSatellite(planetId, satelliteData) {
    return apiClient.post(`/systems/planets/${planetId}/satellites`, satelliteData)
  },

  async getSatellites(planetId) {
    return apiClient.get(`/systems/planets/${planetId}/satellites`)
  },

  // 星云 API
  async getNebulae() {
    return apiClient.get('/nebulae')
  },

  async createNebula(nebulaData) {
    return apiClient.post('/nebulae', nebulaData)
  },

  async condenseNebula(nebulaId) {
    return apiClient.post(`/nebulae/${nebulaId}/condense`)
  },

  // 星团 API
  async getClusters() {
    return apiClient.get('/clusters')
  },

  async createCluster(clusterData) {
    return apiClient.post('/clusters', clusterData)
  },

  async addSystemToCluster(clusterId, systemId) {
    return apiClient.post(`/clusters/${clusterId}/systems/${systemId}`)
  },

  async removeSystemFromCluster(clusterId, systemId) {
    return apiClient.delete(`/clusters/${clusterId}/systems/${systemId}`)
  },

  async getClusterSystems(clusterId) {
    return apiClient.get(`/clusters/${clusterId}/systems`)
  },

  // 关系 API
  async createRelation(relationData) {
    return apiClient.post('/galaxy/relations', relationData)
  },

  async getRelations() {
    return apiClient.get('/galaxy/relations')
  },

  async deleteRelation(fromSystem, toSystem) {
    return apiClient.delete(`/galaxy/relations/${fromSystem}/${toSystem}`)
  },

  // 宇宙网纤维 API
  async createFiber(fiberData) {
    return apiClient.post('/galaxy/fibers', fiberData)
  },

  async getFibers() {
    return apiClient.get('/galaxy/fibers')
  },

  async deleteFiber(fiberId) {
    return apiClient.delete(`/galaxy/fibers/${fiberId}`)
  },
}

export default api
