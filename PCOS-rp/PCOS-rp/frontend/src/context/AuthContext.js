// context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

// Set API base (use env var in production)
const API_BASE = process.env.REACT_APP_API_URL || 'https://pcos-backend-krz0.onrender.com';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // user object from /auth/me
  const [loading, setLoading] = useState(false);

  // Validate token and fetch user
  const fetchCurrentUser = async (token) => {
    if (!token) {
      return null;
    }

    try {
      setLoading(true); // start loading while validating token
      const res = await fetch(`${API_BASE}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        }
      });
      // debug helpful logs (remove in prod)
      console.log('[Auth] fetchCurrentUser status', res.status);

      if (!res.ok) {
        localStorage.removeItem('pcos_token');
        setUser(null);
        return null;
      }
      const data = await res.json().catch(() => null);
      if (data) {
        setUser(data);
        return data;
      } else {
        setUser(null);
        return null;
      }
    } catch (err) {
      console.error('[Auth] fetchCurrentUser error', err);
      setUser(null);
      return null;
    } finally {
      setLoading(false); // validation finished
    }
  };

  // Restore token on startup and validate
  useEffect(() => {
    (async () => {
      const token = localStorage.getItem('pcos_token');
      if (token) {
        await fetchCurrentUser(token);
      } else {
        // ensure loading is false when there's no token
        setLoading(false);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // login: call backend, store token, validate, set user
  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: (email || '').trim().toLowerCase(), password })
      });

      console.log('[Auth] login status', res.status);

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        const message = data.error || data.message || `Login failed (${res.status})`;
        return { success: false, error: message };
      }

      const token = data?.token;
      if (!token) {
        return { success: false, error: 'No token returned from server' };
      }

      // Save token (string) and validate it by calling /auth/me
      localStorage.setItem('pcos_token', token);
      const userObj = await fetchCurrentUser(token);

      if (!userObj) {
        // cleanup if validation fails
        localStorage.removeItem('pcos_token');
        return { success: false, error: 'Token validation failed' };
      }

      return { success: true };
    } catch (err) {
      console.error('[Auth] login error', err);
      return { success: false, error: err.message || 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('pcos_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
