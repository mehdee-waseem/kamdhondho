import { MapPin, Calendar, ExternalLink, Bookmark, BookmarkCheck, Clock } from 'lucide-react'
import { Job } from '../types'

interface JobCardProps {
  job: Job
  isBookmarked: boolean
  onToggleBookmark: () => void
}

export function JobCard({ job, isBookmarked, onToggleBookmark }: JobCardProps) {
  return (
    <div className="card p-6 hover:border-primary-300 dark:hover:border-primary-700">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
            {job.title}
          </h3>
          <p className="text-sm font-medium text-primary-600 dark:text-primary-400 mb-3">
            {job.company}
          </p>

          <div className="flex flex-wrap gap-2 mb-4">
            <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
              <MapPin className="w-4 h-4" />
              {job.location}
            </div>
            <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
              <Calendar className="w-4 h-4" />
              {job.startDate}
            </div>
            <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400">
              <Clock className="w-4 h-4" />
              {job.duration}
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
              <span className="font-medium">Match:</span> {job.matchRationale}
            </p>
          </div>

          <div className="flex flex-wrap gap-1.5 mb-4">
            {job.skills.map(skill => (
              <span
                key={skill}
                className="badge bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        <button
          onClick={onToggleBookmark}
          className="flex-shrink-0 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title={isBookmarked ? 'Remove bookmark' : 'Bookmark this job'}
        >
          {isBookmarked ? (
            <BookmarkCheck className="w-5 h-5 text-primary-600" />
          ) : (
            <Bookmark className="w-5 h-5 text-gray-400" />
          )}
        </button>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
        <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
          <span className="badge bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300">
            {job.platform}
          </span>
          <span>Posted: {job.postedDate}</span>
        </div>
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary flex items-center gap-2 text-sm"
        >
          <ExternalLink className="w-4 h-4" />
          Apply Now
        </a>
      </div>
    </div>
  )
}