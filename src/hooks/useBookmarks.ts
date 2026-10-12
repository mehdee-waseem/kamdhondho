import { useState, useEffect } from 'react'

export function useBookmarks() {
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(() => {
    const saved = localStorage.getItem('kamdhondho_bookmarks')
    return new Set(saved ? JSON.parse(saved) : [])
  })

  useEffect(() => {
    localStorage.setItem('kamdhondho_bookmarks', JSON.stringify([...bookmarkedIds]))
  }, [bookmarkedIds])

  const toggleBookmark = (id: string) => {
    setBookmarkedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  const isBookmarked = (id: string) => bookmarkedIds.has(id)

  return { bookmarkedIds, toggleBookmark, isBookmarked }
}