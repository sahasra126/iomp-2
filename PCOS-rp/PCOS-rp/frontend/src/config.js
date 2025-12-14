// API Configuration
// Change this IP address if your backend is on a different machine
// const API_BASE_URL = 'http://172.20.10.3:5000';

// export default API_BASE_URL;
// create this file (or update existing)
// const API_BASE = process.env.REACT_APP_BACKEND_URL || "https://pcos-backend-bj1v.onrender.com";
// export default API_BASE;
const API_BASE = process.env.REACT_APP_BACKEND_URL;

if (!API_BASE) {
  throw new Error("REACT_APP_BACKEND_URL is not defined");
}

export default API_BASE;
