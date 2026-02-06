import React from "react"

export default function ArticlesList({ articles }) {
  return (
    <div style={styles.list}>
      {articles.map((a, i) => {
        // Calculate a 'Contribution' indicator
        const isNegative = a.sentiment === 'negative';
        const riskWeight = isNegative ? (a.sentiment_score * 100).toFixed(0) : 0;

        return (
          <div key={i} style={styles.articleItem}>
            <div style={styles.meta}>
              <span style={{...styles.sentiment, ...sentimentColors[a.sentiment]}}>
                {a.sentiment?.toUpperCase()}
              </span>
              <span style={styles.category}>{a.category}</span>
              {isNegative && (
                <span style={styles.riskBadge}>RISK IMPACT: {riskWeight}%</span>
              )}
            </div>
            <h4 style={styles.title}>{a.title}</h4>
            <p style={styles.summary}>{a.summary}</p>
          </div>
        );
      })}
    </div>
  )
}

const sentimentColors = {
  positive: { color: '#059669', background: '#ecfdf5' },
  negative: { color: '#dc2626', background: '#fef2f2' },
  neutral: { color: '#d97706', background: '#fffbeb' }
}

const styles = {
  articleItem: { padding: '20px 0', borderBottom: '1px solid #f1f5f9' },
  meta: { display: 'flex', gap: '15px', alignItems: 'center', marginBottom: '10px' },
  sentiment: { fontSize: '10px', fontWeight: '800', padding: '3px 8px', borderRadius: '4px' },
  riskBadge: { fontSize: '9px', fontWeight: 'bold', background: '#0F172A', color: '#fff', padding: '2px 6px', borderRadius: '4px' },
  category: { fontSize: '11px', color: '#2563eb', fontWeight: 'bold', textTransform: 'uppercase' },
  title: { fontSize: '17px', color: '#0f172a', marginBottom: '8px', fontWeight: '700' },
  summary: { fontSize: '14px', color: '#475569', lineHeight: '1.6' }
}