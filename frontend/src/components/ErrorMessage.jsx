import React from 'react';
import { AlertTriangle } from 'lucide-react';

export default function ErrorMessage({ message }) {
  if (!message) return null;

  return (
    <div className="error-banner" role="alert">
      <AlertTriangle size={24} style={{ flexShrink: 0, marginTop: '2px' }} />
      <div>
        <div className="error-title">Analysis Request Failed</div>
        <div style={{ fontSize: '0.88rem', lineHeight: '1.4' }}>{message}</div>
      </div>
    </div>
  );
}
