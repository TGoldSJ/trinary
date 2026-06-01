/**
 * 参星（Trinary）- 搜索栏组件
 */

import { useState } from 'react'

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && onSearch) {
      onSearch(query.trim())
    }
  }

  const handleChange = (e) => {
    setQuery(e.target.value)
  }

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="搜索知识图谱..."
        className="search-input"
      />
      <button type="submit" className="search-button">
        搜索
      </button>
    </form>
  )
}

export default SearchBar
