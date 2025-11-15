// // context/AuthContext.jsx
// import React, { createContext, useContext, useState, useEffect } from 'react';

// const AuthContext = createContext();

// export const useAuth = () => useContext(AuthContext);

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null); // or token
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     // Try to restore user from localStorage (demo only).
//     const token = localStorage.getItem('pcos_token');
//     if (token) {
//       // optionally validate token with backend
//       setUser({ token }); 
//     }
//   }, []);

//   const login = async (email, password) => {
//     setLoading(true);
//     try {
//       // Example fetch - adapt URL and payload to your backend
//       const res = await fetch('/api/auth/login', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ email, password }),
//       });

//       if (!res.ok) {
//         const errData = await res.json().catch(() => ({}));
//         return { success: false, error: errData.message || `Login failed (${res.status})` };
//       }

//       const data = await res.json();
//       // Suppose backend returns { token, user }
//       if (data?.token) {
//         localStorage.setItem('pcos_token', data.token); // demo only
//         setUser(data.user || { token: data.token });
//         return { success: true };
//       } else {
//         return { success: false, error: 'Invalid response from server' };
//       }
//     } catch (err) {
//       return { success: false, error: err.message || 'Network error' };
//     } finally {
//       setLoading(false);
//     }
//   };

//   const logout = () => {
//     localStorage.removeItem('pcos_token');
//     setUser(null);
//   };

//   return (
//     <AuthContext.Provider value={{ user, login, logout, loading }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
// context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

// Set your API base here. Prefer using env var in production:
// e.g. REACT_APP_API_URL=https://pcos-backend-krz0.onrender.com
const API_BASE = process.env.REACT_APP_API_URL || 'https://pcos-backend-krz0.onrender.com';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // will hold user object from /auth/me
  const [loading, setLoading] = useState(false);

  // helper to call /auth/me and set user
  const fetchCurrentUser = async (token) => {
    if (!token) return null;
    try {
      const res = await fetch(`${API_BASE}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        }
      });

      if (!res.ok) {
        // token invalid/expired or other error. Remove saved token.
        console.warn('fetchCurrentUser failed', res.status);
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
      console.error('fetchCurrentUser network error', err);
      setUser(null);
      return null;
    }
  };

  useEffect(() => {
    // Restore token from localStorage and validate it with backend
    const token = localStorage.getItem('pcos_token');
    if (token) {
      // validate token by calling /auth/me
      fetchCurrentUser(token);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        // try to read error body
        const errData = await res.json().catch(() => ({}));
        const message = errData.error || errData.message || `Login failed (${res.status})`;
        return { success: false, error: message };
      }

      const data = await res.json();
      const token = data?.token;
      if (!token) {
        return { success: false, error: 'No token returned from server' };
      }

      // save token and fetch user info
      localStorage.setItem('pcos_token', token);
      const userObj = await fetchCurrentUser(token);

      if (!userObj) {
        // token saved but fetching user failed (maybe token invalid). Cleanup.
        localStorage.removeItem('pcos_token');
        return { success: false, error: 'Failed to validate token with server' };
      }

      return { success: true };
    } catch (err) {
      console.error('login network error', err);
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

