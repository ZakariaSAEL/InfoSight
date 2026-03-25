import { Link, useLocation } from 'react-router-dom';
import { Sun, Moon, FileText, Clock } from 'lucide-react';

export default function Navbar({ theme, toggleTheme }) {
  const location = useLocation();

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '1rem 2rem',
      backgroundColor: 'var(--surface)',
      borderBottom: '1px solid var(--border)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
        <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FileText size={28} color="var(--primary)" />
          <span>InfoSight</span>
        </Link>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link 
            to="/" 
            style={{ 
              color: location.pathname === '/' ? 'var(--primary)' : 'var(--text-muted)',
              fontWeight: location.pathname === '/' ? '600' : '400',
              display: 'flex', alignItems: 'center', gap: '0.5rem'
            }}
          >
            <FileText size={18} /> Upload
          </Link>
          <Link 
            to="/history" 
            style={{ 
              color: location.pathname === '/history' ? 'var(--primary)' : 'var(--text-muted)',
              fontWeight: location.pathname === '/history' ? '600' : '400',
              display: 'flex', alignItems: 'center', gap: '0.5rem'
            }}
          >
            <Clock size={18} /> History
          </Link>
        </div>
      </div>
      
      <button 
        onClick={toggleTheme}
        style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          padding: '0.5rem', borderRadius: '50%', backgroundColor: 'var(--background)'
        }}
        title="Toggle Theme"
      >
        {theme === 'light' ? <Moon size={20} color="var(--text)" /> : <Sun size={20} color="#F59E0B" />}
      </button>
    </nav>
  );
}
