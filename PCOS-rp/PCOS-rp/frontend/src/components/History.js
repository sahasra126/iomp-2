import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import API_BASE_URL from '../config';
import './History.css';

const History = () => {
  const { token, user } = useAuth();
  const [lifestyleHistory, setLifestyleHistory] = useState([]);
  const [clinicalHistory, setClinicalHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      
      // Fetch lifestyle assessment history
      const lifestyleRes = await axios.get(
        `${API_BASE_URL}/lifestyle/prediction-history`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      
      // Fetch clinical prediction history
      const clinicalRes = await axios.get(
        `${API_BASE_URL}/predictions/history`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );

      setLifestyleHistory(lifestyleRes.data.predictions || []);
      setClinicalHistory(clinicalRes.data.predictions || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load history: ' + (err.response?.data?.error || err.message));
      setLoading(false);
    }
  };

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRiskBadgeClass = (riskLevel) => {
    if (typeof riskLevel === 'string') {
      return riskLevel.toLowerCase();
    }
    return '';
  };

  if (loading) {
    return (
      <div className="history-container">
        <div className="loading-spinner">Loading your assessment history...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="history-container">
        <div className="error-box">{error}</div>
      </div>
    );
  }

  const totalAssessments = lifestyleHistory.length + clinicalHistory.length;

  return (
    <div className="history-container">
      <div className="history-header">
        <h1>📊 Your Assessment History</h1>
        <p>Welcome back, {user?.full_name || user?.email}!</p>
        <div className="stats-summary">
          <div className="stat-card">
            <div className="stat-number">{totalAssessments}</div>
            <div className="stat-label">Total Assessments</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{lifestyleHistory.length}</div>
            <div className="stat-label">Lifestyle Assessments</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{clinicalHistory.length}</div>
            <div className="stat-label">Clinical Predictions</div>
          </div>
        </div>
      </div>

      {totalAssessments === 0 ? (
        <div className="no-history">
          <h2>No assessments yet</h2>
          <p>Take your first assessment to see your results here!</p>
        </div>
      ) : (
        <>
          {/* Lifestyle Assessment History */}
          {lifestyleHistory.length > 0 && (
            <section className="history-section">
              <h2>🏃‍♀️ Lifestyle Assessments</h2>
              <div className="history-list">
                {lifestyleHistory.map((assessment) => (
                  <div key={assessment.id} className="history-item">
                    <div className="item-header" onClick={() => toggleExpand(`lifestyle-${assessment.id}`)}>
                      <div className="item-info">
                        <span className={`risk-badge ${getRiskBadgeClass(assessment.risk_level)}`}>
                          {assessment.risk_level} Risk
                        </span>
                        <span className="item-date">{formatDate(assessment.created_at)}</span>
                      </div>
                      <div className="item-stats">
                        <span className="probability">Risk Score: {(assessment.risk_score * 100).toFixed(1)}%</span>
                        <span className="expand-icon">{expandedId === `lifestyle-${assessment.id}` ? '▲' : '▼'}</span>
                      </div>
                    </div>
                    
                    {expandedId === `lifestyle-${assessment.id}` && (
                      <div className="item-details">
                        <h3>Risk Factors</h3>
                        <div className="risk-factors">
                          {assessment.risk_factors && Object.entries(assessment.risk_factors).map(([key, value]) => (
                            <div key={key} className="factor-item">
                              <span className="factor-name">{key}:</span>
                              <span className="factor-value">{value.value}</span>
                              <span className="factor-importance">
                                Importance: {(value.importance * 100).toFixed(1)}%
                              </span>
                            </div>
                          ))}
                        </div>

                        {assessment.recommendations && assessment.recommendations.length > 0 && (
                          <>
                            <h3>Recommendations</h3>
                            <div className="recommendations-list">
                              {assessment.recommendations.map((rec, idx) => (
                                <div key={idx} className={`recommendation-card ${rec.priority}`}>
                                  <h4>{rec.title}</h4>
                                  <p>{rec.description}</p>
                                  {rec.actions && rec.actions.length > 0 && (
                                    <ul>
                                      {rec.actions.map((action, i) => (
                                        <li key={i}>{action}</li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              ))}
                            </div>
                          </>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Clinical Prediction History */}
          {clinicalHistory.length > 0 && (
            <section className="history-section">
              <h2>🔬 Clinical Predictions</h2>
              <div className="history-list">
                {clinicalHistory.map((prediction) => (
                  <div key={prediction.id} className="history-item">
                    <div className="item-header" onClick={() => toggleExpand(`clinical-${prediction.id}`)}>
                      <div className="item-info">
                        <span className={`risk-badge ${getRiskBadgeClass(prediction.risk_level)}`}>
                          {prediction.risk_level || (prediction.prediction_result === 1 ? 'High' : 'Low')} Risk
                        </span>
                        <span className="item-date">{formatDate(prediction.created_at)}</span>
                      </div>
                      <div className="item-stats">
                        <span className="probability">Probability: {(prediction.probability * 100).toFixed(1)}%</span>
                        <span className="expand-icon">{expandedId === `clinical-${prediction.id}` ? '▲' : '▼'}</span>
                      </div>
                    </div>
                    
                    {expandedId === `clinical-${prediction.id}` && (
                      <div className="item-details">
                        <h3>Lab Values</h3>
                        <div className="lab-values">
                          {prediction.input_data && Object.entries(prediction.input_data).map(([key, value]) => (
                            <div key={key} className="lab-item">
                              <span className="lab-name">{key}:</span>
                              <span className="lab-value">{value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
};

export default History;
