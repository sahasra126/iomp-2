// // context/AuthContext.jsx
// import React, { createContext, useContext, useState, useEffect } from 'react';

// const AuthContext = createContext();
// export const useAuth = () => useContext(AuthContext);

// // Set API base (use env var in production)
// const API_BASE = process.env.REACT_APP_API_URL || 'https://pcos-backend-krz0.onrender.com';

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null); // user object from /auth/me
//   const [token, setToken] = useState(null); // store raw token for headers
//   const [loading, setLoading] = useState(true); // start true until we check local token

//   // Validate token and fetch user
//   const fetchCurrentUser = async (t) => {
//     if (!t) {
//       setUser(null);
//       setToken(null);
//       return null;
//     }

//     try {
//       setLoading(true); // start loading while validating token
//       const res = await fetch(`${API_BASE}/auth/me`, {
//         method: 'GET',
//         headers: {
//           'Authorization': `Bearer ${t}`,
//           'Accept': 'application/json'
//         }
//       });
//       console.log('[Auth] fetchCurrentUser status', res.status);

//       if (!res.ok) {
//         // invalid token or other issue
//         localStorage.removeItem('pcos_token');
//         setUser(null);
//         setToken(null);
//         return null;
//       }

//       const data = await res.json().catch(() => null);
//       if (data) {
//         setUser(data);
//         setToken(t);
//         return data;
//       } else {
//         setUser(null);
//         setToken(null);
//         return null;
//       }
//     } catch (err) {
//       console.error('[Auth] fetchCurrentUser error', err);
//       setUser(null);
//       setToken(null);
//       return null;
//     } finally {
//       setLoading(false); // validation finished
//     }
//   };

//   // Restore token on startup and validate
//   useEffect(() => {
//     (async () => {
//       const stored = localStorage.getItem('pcos_token');
//       if (stored) {
//         await fetchCurrentUser(stored);
//       } else {
//         setLoading(false);
//       }
//     })();
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, []);

//   // login: call backend, store token, validate, set user
//   const login = async (email, password) => {
//     setLoading(true);
//     try {
//       const res = await fetch(`${API_BASE}/auth/login`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ email: (email || '').trim().toLowerCase(), password })
//       });

//       console.log('[Auth] login status', res.status);

//       const data = await res.json().catch(() => ({}));

//       if (!res.ok) {
//         const message = data.error || data.message || `Login failed (${res.status})`;
//         return { success: false, error: message };
//       }

//       const t = data?.token;
//       if (!t) {
//         return { success: false, error: 'No token returned from server' };
//       }

//       // Save token and validate it by calling /auth/me
//       localStorage.setItem('pcos_token', t);
//       const userObj = await fetchCurrentUser(t);

//       if (!userObj) {
//         // cleanup if validation fails
//         localStorage.removeItem('pcos_token');
//         setToken(null);
//         return { success: false, error: 'Token validation failed' };
//       }

//       return { success: true };
//     } catch (err) {
//       console.error('[Auth] login error', err);
//       return { success: false, error: err.message || 'Network error' };
//     } finally {
//       setLoading(false);
//     }
//   };

//   const logout = () => {
//     localStorage.removeItem('pcos_token');
//     setToken(null);
//     setUser(null);
//   };

//   return (
//     <AuthContext.Provider value={{ user, token, login, logout, loading }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
// context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

// API base (use env var in production)
const API_BASE = process.env.REACT_APP_API_URL || 'https://pcos-backend-krz0.onrender.com';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);      // user object from /auth/me
  const [token, setToken] = useState(null);    // JWT token string
  const [loading, setLoading] = useState(false);

  // Validate token and fetch user
  const fetchCurrentUser = async (t) => {
    if (!t) return null;
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${t}`,
          'Accept': 'application/json'
        }
      });

      // If token invalid remove it
      if (!res.ok) {
        localStorage.removeItem('pcos_token');
        setToken(null);
        setUser(null);
        return null;
      }

      const data = await res.json().catch(() => null);
      if (data) {
        setUser(data);
        setToken(t);
        localStorage.setItem('pcos_token', t); // ensure stored
        return data;
      } else {
        setUser(null);
        setToken(null);
        localStorage.removeItem('pcos_token');
        return null;
      }
    } catch (err) {
      console.error('[Auth] fetchCurrentUser error', err);
      setUser(null);
      setToken(null);
      localStorage.removeItem('pcos_token');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Restore token on startup and validate
  useEffect(() => {
    (async () => {
      setLoading(true);
      const saved = localStorage.getItem('pcos_token');
      if (saved) {
        await fetchCurrentUser(saved);
      } else {
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

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        const message = data.error || data.message || `Login failed (${res.status})`;
        return { success: false, error: message };
      }

      const t = data?.token;
      if (!t) return { success: false, error: 'No token returned from server' };

      localStorage.setItem('pcos_token', t);
      const userObj = await fetchCurrentUser(t);
      if (!userObj) {
        localStorage.removeItem('pcos_token');
        return { success: false, error: 'Failed to validate token with server' };
      }

      return { success: true };
    } catch (err) {
      console.error('[Auth] login error', err);
      return { success: false, error: err.message || 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  // register: call backend /auth/register, store token, validate using fetchCurrentUser
  // signature matches how your Register component calls it:
  // register(email, password, fullName, age)
  const register = async (email, password, fullName = '', age = null) => {
    setLoading(true);
    try {
      const payload = { email: (email || '').trim().toLowerCase(), password };
      if (fullName) payload.full_name = fullName;
      if (age !== null && age !== undefined) payload.age = age;

      const res = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        const message = data.error || data.message || `Register failed (${res.status})`;
        return { success: false, error: message };
      }

      const t = data?.token;
      if (!t) {
        // fallback: sometimes register returns message only; handle gracefully
        return { success: false, error: 'No token returned from server after registration' };
      }

      // store and validate token
      localStorage.setItem('pcos_token', t);
      const userObj = await fetchCurrentUser(t);
      if (!userObj) {
        localStorage.removeItem('pcos_token');
        return { success: false, error: 'Token validation failed after registration' };
      }

      return { success: true };
    } catch (err) {
      console.error('[Auth] register error', err);
      return { success: false, error: err.message || 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('pcos_token');
    setToken(null);
    setUser(null);
  };

  // expose token too because some components use `const { token } = useAuth()`
  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

