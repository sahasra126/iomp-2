import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import './Navbar.css'

export default function Navbar() {
  const { user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (mobileMenuOpen && !e.target.closest('.navbar-links') && !e.target.closest('.navbar-toggle')) {
        setMobileMenuOpen(false);
      }
      if (showDropdown && !e.target.closest('.user-menu')) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [mobileMenuOpen, showDropdown]);

  // Close mobile menu on route change
  const handleLinkClick = () => {
    setMobileMenuOpen(false);
    setShowDropdown(false);
  };

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [mobileMenuOpen]);

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h2>PCOS Predictor</h2>
      </div>

      {/* Mobile Menu Toggle */}
      <button 
        className={`navbar-toggle ${mobileMenuOpen ? 'active' : ''}`}
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        aria-label="Toggle navigation menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Navigation Links */}
      <ul className={`navbar-links ${mobileMenuOpen ? 'active' : ''}`}>
        <li><Link to="/" onClick={handleLinkClick}>Home</Link></li>
        <li><Link to="/lifestyle-assessment" onClick={handleLinkClick}>Lifestyle Assessment</Link></li>
        <li><Link to="/clinical-prediction" onClick={handleLinkClick}>Clinical Prediction</Link></li>
        <li><Link to="/tracker" onClick={handleLinkClick}>Symptom Tracker</Link></li>
        <li><Link to="/education" onClick={handleLinkClick}>Education</Link></li>
        <li><Link to="/visualization" onClick={handleLinkClick}>Visualization</Link></li>
        
        {/* Mobile Auth Links - shown only on mobile */}
        {user ? (
          <li className="mobile-auth-item">
            <Link to="/history" onClick={handleLinkClick}>📊 History</Link>
          </li>
        ) : (
          <>
            <li className="mobile-auth-item">
              <Link to="/login" onClick={handleLinkClick}>Login</Link>
            </li>
            <li className="mobile-auth-item">
              <Link to="/register" onClick={handleLinkClick}>Register</Link>
            </li>
          </>
        )}
      </ul>

      {/* Auth Section - Desktop */}
      <div className="navbar-auth">
        {user ? (
          <>
            <div className="user-menu">
              <span 
                className="user-greeting" 
                onClick={() => setShowDropdown(!showDropdown)}
              >
                Hello, {user.full_name || user.email} ▾
              </span>
              {showDropdown && (
                <div className="user-dropdown">
                  <Link to="/history" onClick={() => setShowDropdown(false)}>
                    📊 Assessment History
                  </Link>
                  <Link to="/profile" onClick={() => setShowDropdown(false)}>
                    👤 My Profile
                  </Link>
                  <button onClick={logout} className="dropdown-logout">
                    🚪 Logout
                  </button>
                </div>
              )}
            </div>
            <button onClick={logout} className="logout-btn">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="auth-link">Login</Link>
            <Link to="/register" className="auth-link register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
