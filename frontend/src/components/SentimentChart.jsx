import React from "react"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts"

export default function SentimentChart({ metrics }) {
  return (
    <div style={{ height: 350, width: '100%' }}>
      <ResponsiveContainer>
        <LineChart data={metrics}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} dy={10} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} domain={[-1, 1]} />
          <Tooltip contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
          <Line type="monotone" dataKey="avg_sentiment" stroke="#2563eb" strokeWidth={3} dot={{ r: 4, fill: '#2563eb', stroke: '#fff', strokeWidth: 2 }} activeDot={{ r: 6 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}