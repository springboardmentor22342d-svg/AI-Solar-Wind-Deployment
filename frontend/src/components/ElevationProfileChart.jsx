import React, { useMemo } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export default function ElevationProfileChart({ centerElevation }) {
  // Generate a mock elevation profile using the center elevation
  const data = useMemo(() => {
    if (!centerElevation) return [];
    const points = [];
    let currentElev = centerElevation - 50; // Start slightly lower
    
    for (let i = 0; i <= 20; i++) {
      // Simulate terrain bumps
      const randomVariance = (Math.random() - 0.5) * 30;
      currentElev += randomVariance;
      
      // Force it to hit centerElevation at the middle
      if (i === 10) {
        currentElev = centerElevation;
      }
      
      points.push({
        distance: `${(i * 5).toFixed(0)} km`,
        elevation: Math.max(0, Math.round(currentElev))
      });
    }
    return points;
  }, [centerElevation]);

  if (!data || data.length === 0) return null;

  return (
    <div className="card" style={{ height: '300px', padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
        Site Elevation Profile (West-East Cross-Section)
      </h3>
      <div style={{ flex: 1, minHeight: 0 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
            <defs>
              <linearGradient id="colorElevation" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--bg-border)" />
            <XAxis dataKey="distance" axisLine={false} tickLine={false} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
            <Tooltip
              contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--bg-border)', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--color-green)', fontWeight: 'bold' }}
              labelStyle={{ color: 'var(--text-secondary)', marginBottom: '4px' }}
              formatter={(value) => [`${value} m`, 'Elevation']}
            />
            <Area type="monotone" dataKey="elevation" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorElevation)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
