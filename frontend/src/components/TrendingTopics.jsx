import React from "react"

export default function TrendingTopics({ topics }) {
  return (
    <div style={styles.container}>
      <div style={styles.tagContainer}>
        {topics.map((t, i) => (
          <div key={i} style={styles.badge}>
            <span style={styles.hashtag}>#</span>
            <span style={styles.tagName}>{t[0]}</span>
            <span style={styles.count}>{t[1]}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

const styles = {
  container: { width: '100%' },
  tagContainer: { display: 'flex', flexWrap: 'wrap', gap: '8px' },
  badge: { background: '#f1f5f9', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '6px 12px', display: 'flex', alignItems: 'center', gap: '6px' },
  hashtag: { color: '#2563eb', fontWeight: 'bold', fontSize: '14px' },
  tagName: { fontSize: '13px', color: '#1e293b', fontWeight: '600' },
  count: { background: '#e2e8f0', color: '#475569', fontSize: '10px', padding: '2px 6px', borderRadius: '4px', fontWeight: 'bold' }
}