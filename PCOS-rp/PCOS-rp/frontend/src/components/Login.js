// context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // or token
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Try to restore user from localStorage (demo only).
    const token = localStorage.getItem('pcos_token');
    if (token) {
      // optionally validate token with backend
      setUser({ token }); 
    }
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      // Example fetch - adapt URL and payload to your backend
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        return { success: false, error: errData.message || `Login failed (${res.status})` };
      }

      const data = await res.json();
      // Suppose backend returns { token, user }
      if (data?.token) {
        localStorage.setItem('pcos_token', data.token); // demo only
        setUser(data.user || { token: data.token });
        return { success: true };
      } else {
        return { success: false, error: 'Invalid response from server' };
      }
    } catch (err) {
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
