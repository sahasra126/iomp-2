// // import logo from './logo.svg';
// // import './App.css';

// // function App() {
// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         <img src={logo} className="App-logo" alt="logo" />
// //         <p>
// //           Edit <code>src/App.js</code> and save to reload.
// //         </p>
// //         <a
// //           className="App-link"
// //           href="https://reactjs.org"
// //           target="_blank"
// //           rel="noopener noreferrer"
// //         >
// //           Learn React
// //         </a>
// //       </header>
// //     </div>
// //   );
// // }

// // export default App;

// import PCOSForm from "./components/PCOSForm";

// function App() {
//   return <PCOSForm />;
// }

// export default App;

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import PCOSForm from "./components/PCOSForm";
import LifestyleAssessment from "./components/LifestyleAssessment";
import Education from "./components/Education";
import Visualization from "./components/Visualization";
import SymptomTracker from "./components/SymptomTracker";
import History from "./components/History";
import Login from "./components/Login";
import Register from "./components/Register";
import "./App.css";

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  return user ? children : <Navigate to="/login" />;
};

function AppRoutes() {
  return (
    <>
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/lifestyle-assessment" 
            element={
              <ProtectedRoute>
                <LifestyleAssessment />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/clinical-prediction" 
            element={
              <ProtectedRoute>
                <PCOSForm />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/predict" 
            element={<Navigate to="/lifestyle-assessment" replace />}
          />
          <Route path="/education" element={<Education />} />
          <Route path="/visualization" element={<Visualization />} />
          <Route 
            path="/tracker" 
            element={
              <ProtectedRoute>
                <SymptomTracker />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/history" 
            element={
              <ProtectedRoute>
                <History />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </div>
    </>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
