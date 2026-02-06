import React, { useState } from "react"
import axios from "axios"
import SentimentChart from "../components/SentimentChart"
import ESGPieChart from "../components/ESGPieChart"
import TrendingTopics from "../components/TrendingTopics"
import ArticlesList from "../components/ArticlesList"
import SentimentBarChart from "../components/SentimentBarChart"

const API = "http://127.0.0.1:5001"

export default function Dashboard() {
  const [company, setCompany] = useState("")
  const [articles, setArticles] = useState([])
  const [metrics, setMetrics] = useState([])
  const [trending, setTrending] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  
  const [confidence, setConfidence] = useState(0)
  const [alert, setAlert] = useState({ level: "STABLE", message: "System Monitoring Active", color: "#10B981" })

  const fetchCompanyData = async () => {
    if (!company) return window.alert("Enter a company name")
    setLoading(true)
    setError("")

    try {
      await axios.get(`${API}/fetch/${company}`)
      
      const [artRes, metRes, trendRes, riskRes] = await Promise.all([
        axios.get(`${API}/articles/${company}`),
        axios.get(`${API}/metrics/${company}`),
        axios.get(`${API}/trending/${company}`),
        axios.get(`${API}/risk/${company}`)
      ])

      setArticles(artRes.data.articles || [])
      setConfidence(artRes.data.overall_confidence || 0)
      setMetrics(metRes.data.metrics || [])
      setTrending(trendRes.data.trending_topics || [])
      setAlert(riskRes.data)
    } catch (err) {
      setError("Connection failed. Check if Flask is running on Port 5001.")
    }
    setLoading(false)
  }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.container}>
          {/* UPDATED LOGO: CORE SIGNS */}
          <div style={styles.logo}>
            ESGCORE<span style={styles.logoAccent}>SIGNS</span>
          </div>
          <div style={styles.searchBox}>
            <input
              type="text"
              placeholder="Search Company (e.g. Tesla, Microsoft)"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              style={styles.input}
            />
            <button onClick={fetchCompanyData} style={styles.button} disabled={loading}>
              {loading ? "ANALYZING..." : "RUN AI ENGINE"}
            </button>
          </div>
        </div>
      </header>

      <div style={styles.container}>
        {error && <div style={styles.errorBar}>{error}</div>}

        <div style={{...styles.alertBanner, borderLeftColor: alert.color, backgroundColor: `${alert.color}10`}}>
           <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
              <div style={{...styles.alertIcon, backgroundColor: alert.color}}>!</div>
              <div>
                <span style={{ ...styles.alertLevel, color: alert.color }}>{alert.level}</span>
                <div style={styles.alertMessage}>{alert.message}</div>
              </div>
           </div>
           <div style={styles.livePulse}>
              <div style={{...styles.pulseDot, backgroundColor: alert.color}}></div>
              LIVE SIGNAL
           </div>
        </div>

        <div style={styles.summaryRow}>
           <div style={{...styles.miniCard, borderTop: '4px solid #3b82f6'}}>
             <span style={styles.label}>SENTIMENT SCORE</span>
             <span style={{...styles.value, color: "#2563EB"}}>
                {metrics.length > 0 ? metrics[metrics.length-1].avg_sentiment : "0.00"}
             </span>
           </div>
           <div style={{...styles.miniCard, borderTop: '4px solid #10b981'}}>
             <span style={styles.label}>TOTAL SIGNALS</span>
             <span style={styles.value}>{articles.length} Reports</span>
           </div>
           <div style={{...styles.miniCard, borderTop: '4px solid #8b5cf6'}}>
             <span style={styles.label}>AI CONFIDENCE</span>
             <span style={{...styles.value, color: "#8b5cf6"}}>{confidence}%</span> 
           </div>
        </div>

        <div style={styles.dashboardGrid}>
          <div style={styles.mainCol}>
            <div style={styles.card}>
              <h3 style={styles.cardHeader}>Market Trajectory</h3>
              <div style={{height: '350px'}}>
                 <SentimentChart metrics={metrics} />
              </div>
            </div>
            
            <div style={styles.card}>
              <h3 style={styles.cardHeader}>Intelligence Stream</h3>
              <ArticlesList articles={articles} />
            </div>
          </div>

          <div style={styles.sideCol}>
            <div style={styles.card}>
               <h3 style={styles.cardHeader}>Signal Keywords</h3>
               <TrendingTopics topics={trending} />
            </div>

            <div style={{ ...styles.card, marginTop: "24px" }}>
              <h3 style={styles.cardHeader}>ESG Pillar Weight</h3>
              <ESGPieChart articles={articles} />
            </div>

            <div style={{ ...styles.card, marginTop: "24px" }}>
               <h3 style={styles.cardHeader}>Volume Analytics</h3>
               {/* Restored Usage of SentimentBarChart */}
               <SentimentBarChart articles={articles} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: { background: '#F0F4F8', minHeight: '100vh', color: '#1E293B', fontFamily: "'Inter', sans-serif", paddingBottom: '50px' },
  container: { maxWidth: '1440px', margin: '0 auto', padding: '0 25px' },
  header: { background: 'rgba(255, 255, 255, 0.9)', backdropFilter: 'blur(10px)', padding: "15px 0", borderBottom: "1px solid #E2E8F0", marginBottom: "25px", position: "sticky", top: 0, zIndex: 100 },
  logo: { fontSize: "26px", fontWeight: "900", letterSpacing: "-1.5px", color: "#0F172A", display: 'flex', alignItems: 'center' },
  logoAccent: { 
    background: "linear-gradient(135deg, #6366F1 0%, #A855F7 100%)", 
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginLeft: "4px"
  },
  searchBox: { display: "flex", gap: "12px" },
  input: { background: "#FFFFFF", border: "2px solid #E2E8F0", color: "#0F172A", padding: "12px 20px", borderRadius: "10px", width: "350px", fontSize: "14px" },
  button: { background: "linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)", color: "white", border: "none", padding: "12px 28px", borderRadius: "10px", fontWeight: "700", cursor: "pointer", boxShadow: "0 4px 12px rgba(37, 99, 235, 0.3)" },
  alertBanner: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '18px 25px', borderRadius: '15px', marginBottom: '25px', borderLeft: '8px solid', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.05)' },
  alertIcon: { width: '30px', height: '30px', borderRadius: '50%', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '900', fontSize: '18px' },
  alertLevel: { fontSize: '12px', fontWeight: '900', letterSpacing: '1px' },
  alertMessage: { fontSize: '16px', fontWeight: '700', color: '#1E293B' },
  livePulse: { display: 'flex', alignItems: 'center', gap: '8px', fontSize: '11px', fontWeight: '800', color: '#64748B' },
  pulseDot: { width: '8px', height: '8px', borderRadius: '50%' },
  summaryRow: { display: 'flex', gap: '25px', marginBottom: '30px' },
  miniCard: { flex: 1, background: '#FFFFFF', padding: '25px', borderRadius: '18px', display: 'flex', flexDirection: 'column', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' },
  label: { fontSize: '12px', fontWeight: '700', color: '#64748B', marginBottom: '10px' },
  value: { fontSize: '24px', fontWeight: '900', color: '#0F172A' },
  dashboardGrid: { display: "grid", gridTemplateColumns: "1fr 400px", gap: "30px" },
  card: { background: "#FFFFFF", padding: "28px", borderRadius: '20px', boxShadow: "0 10px 25px -5px rgba(0,0,0,0.05)", border: '1px solid #F1F5F9' },
  cardHeader: { fontSize: "15px", fontWeight: "800", color: "#334155", marginBottom: "25px", letterSpacing: '-0.3px' },
  errorBar: { background: "#FFF1F2", color: "#E11D48", padding: "15px", borderRadius: "12px", marginBottom: "25px", border: "1px solid #FDA4AF", fontWeight: '600' }
}