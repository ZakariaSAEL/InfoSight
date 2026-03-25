import { useState } from 'react';
import { MapPin, FileJson, CheckCircle, AlertTriangle } from 'lucide-react';

export default function ResultCard({ data }) {
  const [showRaw, setShowRaw] = useState(false);

  const getConfidenceColor = (score) => {
    if (!score && score !== 0) return 'var(--text-muted)';
    if (score >= 0.9) return 'var(--success)';
    if (score >= 0.6) return 'var(--warning)';
    return 'var(--error)';
  };

  const getConfidenceIcon = (score) => {
    if (!score && score !== 0) return null;
    if (score >= 0.8) return <CheckCircle size={16} color="var(--success)" />;
    return <AlertTriangle size={16} color="var(--warning)" />;
  };

  return (
    <div className="card" style={{ marginTop: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CheckCircle color="var(--success)" /> Extraction Complete
        </h2>
        <button className="btn-secondary" onClick={() => setShowRaw(!showRaw)} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FileJson size={18} /> {showRaw ? 'Show Structured' : 'Show Raw JSON'}
        </button>
      </div>

      {showRaw ? (
        <pre style={{ backgroundColor: 'var(--background)', padding: '1rem', borderRadius: '8px', overflowX: 'auto', border: '1px solid var(--border)', fontSize: '0.9rem' }}>
          {JSON.stringify(data.raw_data, null, 2)}
        </pre>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
          <DataField label="Invoice Number" value={data.invoice_number} confidence={data.confidence?.invoice_number} icon={getConfidenceIcon} color={getConfidenceColor} />
          <DataField label="Date" value={data.date} confidence={data.confidence?.date} icon={getConfidenceIcon} color={getConfidenceColor} />
          <DataField label="Total Amount" value={data.total} confidence={data.confidence?.total_amount} icon={getConfidenceIcon} color={getConfidenceColor} />
          <DataField label="Vendor Name" value={data.vendor} confidence={data.confidence?.vendor_name} icon={getConfidenceIcon} color={getConfidenceColor} />
          
          <div style={{ gridColumn: '1 / -1', backgroundColor: 'var(--background)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Normalized Address</h4>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <p style={{ fontWeight: '500', fontSize: '1.1rem' }}>{data.address || 'Address not found'}</p>
              {data.address && (
                <a 
                  href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(data.address)}`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--primary)', fontWeight: 'bold' }}
                >
                  <MapPin size={18} /> View on Map
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function DataField({ label, value, confidence, icon, color }) {
  return (
    <div style={{ backgroundColor: 'var(--background)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
      <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>{label}</h4>
      <p style={{ fontWeight: '600', fontSize: '1.25rem', marginBottom: '0.5rem' }}>{value || 'N/A'}</p>
      {confidence !== undefined && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: color(confidence) }}>
          {icon(confidence)}
          <span>Confidence: {(confidence * 100).toFixed(0)}%</span>
        </div>
      )}
    </div>
  );
}
