import { Loader2 } from 'lucide-react';

export default function Loader({ message = "Processing with Gemini 3 AI..." }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '3rem',
      backgroundColor: 'var(--surface)',
      borderRadius: '12px',
      border: '1px solid var(--border)',
      marginTop: '2rem'
    }}>
      <Loader2 size={48} color="var(--primary)" style={{ animation: 'spin 1.5s linear infinite' }} />
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
      <h3 style={{ marginTop: '1.5rem', color: 'var(--text)' }}>{message}</h3>
      <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem', textAlign: 'center' }}>
        Analyzing layout, extracting text, and normalizing Moroccan addresses.
      </p>
    </div>
  );
}
