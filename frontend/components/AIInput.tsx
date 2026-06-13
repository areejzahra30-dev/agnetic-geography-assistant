import React, { useState } from 'react'
import styles from './AIInput.module.css'

interface AIInputProps {
  onSubmit: (text: string) => void
  loading?: boolean
}

export default function AIInput({ onSubmit, loading = false }: AIInputProps) {
  const [text, setText] = useState('')
  const [isLoading, setIsLoading] = useState(loading)

  const handle = async (e?: React.FormEvent) => {
    e?.preventDefault()
    if (!text.trim()) return
    
    setIsLoading(true)
    try {
      await onSubmit(text.trim())
      setText('')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handle} className={styles.form}>
      <div className={styles.wrapper}>
        <label htmlFor="query" className={styles.label}>
          Ask about a place
        </label>
        <div className={styles.inputGroup}>
          <input
            id="query"
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g., Islamabad, Pakistan"
            className={styles.input}
            disabled={isLoading}
            aria-label="Search for a place"
            aria-describedby="query-hint"
          />
          <button
            type="submit"
            disabled={isLoading || !text.trim()}
            className={`${styles.button} btn-primary`}
            aria-label={isLoading ? 'Searching...' : 'Search for place information'}
          >
            {isLoading ? (
              <>
                <span className={styles.spinner} />
                Searching…
              </>
            ) : (
              'Search'
            )}
          </button>
        </div>
        <p id="query-hint" className={styles.hint}>
          Enter a city, state, or country name to explore
        </p>
      </div>
    </form>
  )
}
