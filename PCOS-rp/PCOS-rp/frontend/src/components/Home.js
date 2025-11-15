import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-container">

      {/* Hero Section */}
      <section className="hero-section text-center">
        <div className="hero-content">
          <h1>PCOS Risk Predictor</h1>
          <p>Assess your risk of PCOS with AI-based predictions, learn about PCOS, and visualize trends.</p>
          <Link to="/predict" className="btn btn-gradient btn-lg">
            Start Assessment
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section container">
        <h2 className="section-title text-center">Features</h2>
        <div className="row mt-4">
          <div className="col-md-4 mb-4">
            <div className="feature-card p-4 shadow-sm">
              <h3>AI-Based Prediction</h3>
              <p>Get personalized PCOS risk predictions based on your medical parameters.</p>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="feature-card p-4 shadow-sm">
              <h3>Educational Insights</h3>
              <p>Learn about symptoms, causes, and management of PCOS to stay informed.</p>
            </div>
          </div>
          <div className="col-md-4 mb-4">
            <div className="feature-card p-4 shadow-sm">
              <h3>Visual Analytics</h3>
              <p>View interactive charts to understand your risk trends and probabilities.</p>
            </div>
          </div>
        </div>
      </section>

   

      {/* Footer */}
      <footer className="footer-section text-center py-3 mt-5">
        <p>&copy; {new Date().getFullYear()} PCOS Risk Predictor. All Rights Reserved.</p>
      </footer>
    </div>
  );
}
