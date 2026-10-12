import { RefreshCw, Archive, Inbox, Loader2, AlertCircle, Briefcase } from 'lucide-react'
import { Navbar } from './components/Navbar'
import { FilterBar } from './components/FilterBar'
import { JobCard } from './components/JobCard'
import { useTheme } from './hooks/useTheme'
import { useJobs } from './hooks/useJobs'
import { useBookmarks } from './hooks/useBookmarks'

export default function App() {
  const { darkMode, toggleDarkMode } = useTheme()
  const {
    activeJobs,
    archiveJobs,
    currentView,
    setView,
    filters,
    setFilters,
    loading,
    error,
    lastUpdated,
    totalFound,
    refresh,
    getCountries,
    getSkills,
    getPlatforms
  } = useJobs()
  const { toggleBookmark, isBookmarked } = useBookmarks()

  const currentJobs = currentView === 'active' ? activeJobs : archiveJobs

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3em font-bold text-gray-900 dark:text-white mb-2">
            European Internship Jobs
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Personalized internship opportunities matching your skills in Software Engineering, IoT Security, Smart Mobility & Optimization
          </p>
          {lastUpdated && (
            <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
              <span>Last updated: {new Date(lastUpdated).toLocaleString()}</span>
              <span>{totalFound} jobs found</span>
              <button
                onClick={refresh}
                className="flex items-center gap-1 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh
              </button>
            </div>
          )}
        </div>

        {/* View Toggle */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setView('active')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
              currentView === 'active'
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700'
            }`}
          >
            <Inbox className="w-4 h-4" />
            Active Jobs ({activeJobs.length})
          </button>
          <button
            onClick={() => setView('archive')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
              currentView === 'archive'
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700'
            }`}
          >
            <Archive className="w-4 h-4" />
            All-Time Archive ({archiveJobs.length})
          </button>
        </div>

        {/* Filters */}
        <FilterBar
          filters={filters}
          onFilterChange={setFilters}
          countries={getCountries()}
          skills={getSkills()}
          platforms={getPlatforms()}
        />

        {/* Jobs List */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">Loading jobs...</p>
          </div>
        ) : error ? (
          <div className="card p-6 flex items-center gap-4">
            <AlertCircle className="w-8 h-8 text-red-500 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Error Loading Jobs</h3>
              <p className="text-gray-600 dark:text-gray-400">{error}</p>
            </div>
          </div>
        ) : currentJobs.length === 0 ? (
          <div className="card p-12 text-center">
            <Briefcase className="w-16 h-16 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              No jobs found
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              {filters.search || filters.country || filters.skill || filters.platform
                ? 'Try adjusting your filters'
                : 'Check back later for new opportunities'}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {currentJobs.map(job => (
              <JobCard
                key={job.id}
                job={job}
                isBookmarked={isBookmarked(job.id)}
                onToggleBookmark={() => toggleBookmark(job.id)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Kamdhondho | Personalized European Internship Job Board | Updated Daily
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
            Built for Software Engineering, IoT Security, Smart Mobility & Optimization professionals
          </p>
        </div>
      </footer>
    </div>
  )
}