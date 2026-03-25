import { Lock, X } from 'lucide-react';

export default function LoginModal({ onClose }) {
  
  const handleMockLogin = (e) => {
    e.preventDefault();
    // Simulate successful login 
    localStorage.setItem('isLoggedIn', 'true');
    window.location.reload(); // Reload to refresh state
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.6)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
    }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px', position: 'relative', animation: 'fadeIn 0.2s ease-out' }}>
        <button 
          onClick={onClose}
          style={{ position: 'absolute', top: '1rem', right: '1rem', color: 'var(--text-muted)' }}
        >
          <X size={24} />
        </button>

        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ 
            backgroundColor: 'var(--background)', 
            width: '64px', height: '64px', 
            borderRadius: '50%', 
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 1rem',
            border: '1px solid var(--border)'
          }}>
            <Lock size={32} color="var(--primary)" />
          </div>
          <h2 style={{ marginBottom: '0.5rem' }}>Export Limit Reached</h2>
          <p style={{ color: 'var(--text-muted)' }}>
            You've used your 2 free exports. Please log in or create an account to unlock unlimited history backups and features.
          </p>
        </div>

        <form onSubmit={handleMockLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Email / Username</label>
            <input 
              type="text" 
              required
              placeholder="admin@infosight.com"
              style={{
                width: '100%', padding: '0.75rem', borderRadius: '8px',
                border: '1px solid var(--border)', backgroundColor: 'var(--background)',
                color: 'var(--text)', fontFamily: 'inherit'
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Password</label>
            <input 
              type="password" 
              required
              placeholder="••••••••"
              style={{
                width: '100%', padding: '0.75rem', borderRadius: '8px',
                border: '1px solid var(--border)', backgroundColor: 'var(--background)',
                color: 'var(--text)', fontFamily: 'inherit'
              }}
            />
          </div>
          
          <button type="submit" className="btn-primary" style={{ marginTop: '1rem', width: '100%' }}>
            Unlock Unlimited Access
          </button>
        </form>

        <style>
          {`
            @keyframes fadeIn {
              from { opacity: 0; transform: translateY(10px); }
              to { opacity: 1; transform: translateY(0); }
            }
          `}
        </style>
      </div>
    </div>
  );
}
