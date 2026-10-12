import { Search, Filter } from 'lucide-react'
import { JobFilters } from '../types'

interface FilterBarProps {
  filters: JobFilters
  onFilterChange: (filters: JobFilters) => void
  countries: string[]
  skills: string[]
  platforms: string[]
}

export function FilterBar({ filters, onFilterChange, countries, skills, platforms }: FilterBarProps) {
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilterChange({ ...filters, search: e.target.value })
  }

  const handleSelect = (key: keyof JobFilters) => (e: React.ChangeEvent<HTMLSelectElement>) => {
    onFilterChange({ ...filters, [key]: e.target.value })
  }

  return (
    <div className="card p-4 mb-6">
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-5 h-5 text-primary-600" />
        <h2 className="font-semibold text-gray-900 dark:text-white">Filters</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={filters.search}
            onChange={handleSearch}
            placeholder="Search jobs, companies, skills..."
            className="input-field pl-10"
          />
        </div>

        <select
          value={filters.country}
          onChange={handleSelect('country')}
          className="input-field"
        >
          <option value="">All Countries</option>
          {countries.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select
          value={filters.skill}
          onChange={handleSelect('skill')}
          className="input-field"
        >
          <option value="">All Skills</option>
          {skills.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        <select
          value={filters.platform}
          onChange={handleSelect('platform')}
          className="input-field"
        >
          <option value="">All Platforms</option>
          {platforms.map(p => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
      </div>
    </div>
  )
}