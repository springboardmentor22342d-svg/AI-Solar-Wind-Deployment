import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

export default function MonthlyYieldChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="card" style={{ height: '400px', padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
        12-Month Projected Energy Generation Output
      </h3>
      <div style={{ flex: 1, minHeight: 0 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--bg-border)" />
            <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: 'var(--text-secondary)' }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: 'var(--text-secondary)' }} />
            <Tooltip
              contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--bg-border)', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--text-primary)' }}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" />
            <Bar dataKey="solar_gwh" name="Solar Yield (GWh)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            <Bar dataKey="wind_gwh" name="Wind Yield (GWh)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
