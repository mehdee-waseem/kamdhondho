import { useState, useEffect, useCallback } from 'react'
import { Job, JobData, JobFilters } from '../types'

export function useJobs() {
  const [activeJobs, setActiveJobs] = useState<Job[]>([])
  const [archiveJobs, setArchiveJobs] = useState<Job[]>([])
  const [lastUpdated, setLastUpdated] = useState<string>('')
  const [totalFound, setTotalFound] = useState<number>(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [view, setView] = useState<'active' | 'archive'>('active')
  const [filters, setFilters] = useState<JobFilters>({
    search: '',
    country: '',
    skill: '',
    platform: ''
  })

  const fetchJobs = useCallback(async () => {
    try {
      setLoading(true)
      const [jobsRes, archiveRes] = await Promise.all([
        fetch('/jobs.json'),
        fetch('/archive.json')
      ])

      if (jobsRes.ok) {
        const data: JobData = await jobsRes.json()
        setActiveJobs(data.jobs)
        setLastUpdated(data.lastUpdated)
        setTotalFound(data.totalFound)
      }

      if (archiveRes.ok) {
        const data: { jobs: Job[] } = await archiveRes.json()
        setArchiveJobs(data.jobs)
      }

      setError(null)
    } catch (e) {
      setError('Failed to load jobs. Check console for details.')
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchJobs()
  }, [fetchJobs])

  const filteredJobs = (jobs: Job[]) => {
    return jobs.filter(job => {
      if (filters.search) {
        const search = filters.search.toLowerCase()
        const matches = job.title.toLowerCase().includes(search) ||
          job.company.toLowerCase().includes(search) ||
          job.location.toLowerCase().includes(search) ||
          job.skills.some(s => s.toLowerCase().includes(search))
        if (!matches) return false
      }
      if (filters.country && job.country !== filters.country) return false
      if (filters.skill && !job.skills.includes(filters.skill)) return false
      if (filters.platform && job.platform !== filters.platform) return false
      return true
    })
  }

  const getCountries = () => {
    return [...new Set([...activeJobs, ...archiveJobs].map(j => j.country))].sort()
  }

  const getSkills = () => {
    return [...new Set([...activeJobs, ...archiveJobs].flatMap(j => j.skills))].sort()
  }

  const getPlatforms = () => {
    return [...new Set([...activeJobs, ...archiveJobs].map(j => j.platform))].sort()
  }

  return {
    activeJobs: filteredJobs(activeJobs),
    archiveJobs: filteredJobs(archiveJobs),
    currentView: view,
    setView,
    filters,
    setFilters,
    loading,
    error,
    lastUpdated,
    totalFound,
    refresh: fetchJobs,
    getCountries,
    getSkills,
    getPlatforms
  }
}