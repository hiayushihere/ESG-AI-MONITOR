import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const COLORS = { POSITIVE: "#10b981", NEGATIVE: "#ef4444", NEUTRAL: "#f59e0b" };

export default function SentimentBarChart({ articles }) {
  const dataMap = articles.reduce((acc, art) => {
    const s = (art.sentiment || "neutral").toUpperCase();
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, { POSITIVE: 0, NEGATIVE: 0, NEUTRAL: 0 });

  const data = Object.keys(dataMap).map(key => ({ name: key, value: dataMap[key] }));

  return (
    <div style={{ height: 250, width: '100%' }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <Tooltip cursor={{fill: '#f1f5f9'}} contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px' }} />
          <Bar dataKey="value" radius={[4, 4, 0, 0]} barSize={35}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}