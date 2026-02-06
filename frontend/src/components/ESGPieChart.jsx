import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = { Environmental: "#10b981", Social: "#f59e0b", Governance: "#3b82f6", Other: "#94a3b8" };

export default function ESGPieChart({ articles }) {
  const categoryCounts = articles.reduce((acc, art) => {
    const cat = art.category || "Other";
    acc[cat] = (acc[cat] || 0) + 1;
    return acc;
  }, {});

  const data = Object.keys(categoryCounts).map(name => ({ name, value: categoryCounts[name] }));

  return (
    <div style={styles.wrapper}>
      <div style={styles.chartContainer}>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={data} innerRadius={70} outerRadius={90} paddingAngle={5} dataKey="value" stroke="none">
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name] || COLORS.Other} />
              ))}
            </Pie>
            <Tooltip contentStyle={styles.tooltip} />
          </PieChart>
        </ResponsiveContainer>
        <div style={styles.centerText}>
          <span style={styles.totalNum}>{articles.length}</span>
          <span style={styles.totalLabel}>SIGNALS</span>
        </div>
      </div>
      <div style={styles.legendGrid}>
        {data.map((entry, i) => (
          <div key={i} style={styles.legendItem}>
            <div style={{ ...styles.dot, backgroundColor: COLORS[entry.name] }} />
            <span style={styles.legendName}>{entry.name}</span>
            <span style={styles.legendValue}>{entry.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  wrapper: { width: '100%' },
  chartContainer: { position: 'relative', height: '250px' },
  centerText: { position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center' },
  totalNum: { fontSize: '28px', fontWeight: '800', color: '#0f172a' },
  totalLabel: { fontSize: '10px', color: '#64748b', fontWeight: 'bold' },
  tooltip: { background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#0f172a' },
  legendGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginTop: '10px' },
  legendItem: { display: 'flex', alignItems: 'center', gap: '8px', background: '#f8fafc', padding: '8px', borderRadius: '8px', border: '1px solid #e2e8f0' },
  dot: { width: '8px', height: '8px', borderRadius: '50%' },
  legendName: { fontSize: '11px', color: '#475569', flex: 1 },
  legendValue: { fontSize: '11px', color: '#0f172a', fontWeight: 'bold' }
};