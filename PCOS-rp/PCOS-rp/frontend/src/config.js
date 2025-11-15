// API Configuration
// Change this IP address if your backend is on a different machine
// const API_BASE_URL = 'http://172.20.10.3:5000';

// export default API_BASE_URL;
// create this file (or update existing)
const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000";
export default API_BASE;
