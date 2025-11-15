import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import API_BASE_URL from '../config';
import "./PCOSForm.css";
import Visualization from "./Visualization";

export default function PCOSForm() {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    Age: "",
    BMI: "",
    Insulin: "",
    Testosterone: "",
    LH: "",
    FSH: "",
    Glucose: "",
    Cholesterol: ""
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState(null);

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setApiStatus(response.data);
    } catch (err) {
      setApiStatus({ status: "offline", error: "API server not running" });
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const validateForm = () => {
    const requiredFields = Object.keys(formData);
    const emptyFields = requiredFields.filter(field => !formData[field]);
    
    if (emptyFields.length > 0) {
      setError(`Please fill in all fields: ${emptyFields.join(", ")}`);
      return false;
    }

    // Basic range validation
    const validations = {
      Age: { min: 15, max: 50 },
      BMI: { min: 15, max: 50 },
      Insulin: { min: 1, max: 100 },
      Testosterone: { min: 10, max: 150 },
      LH: { min: 1, max: 50 },
      FSH: { min: 1, max: 30 },
      Glucose: { min: 50, max: 300 },
      Cholesterol: { min: 100, max: 400 }
    };

    for (const [field, range] of Object.entries(validations)) {
      const value = parseFloat(formData[field]);
      if (value < range.min || value > range.max) {
        setError(`${field} should be between ${range.min} and ${range.max}`);
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert string values to numbers
      const numericData = {};
      Object.keys(formData).forEach(key => {
        numericData[key] = parseFloat(formData[key]);
      });

      const response = await axios.post(`${API_BASE_URL}/predict`, numericData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      setResult(response.data);
    } catch (err) {
      if (err.response) {
        setError(`Prediction failed: ${err.response.data.error || err.response.data}`);
      } else if (err.request) {
        setError("Cannot connect to server. Please make sure the backend is running.");
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      Age: "",
      BMI: "",
      Insulin: "",
      Testosterone: "",
      LH: "",
      FSH: "",
      Glucose: "",
      Cholesterol: ""
    });
    setResult(null);
    setError(null);
  };

  const fillSampleData = (riskLevel) => {
    const sampleData = {
      low: {
        Age: "25", BMI: "21", Insulin: "8", Testosterone: "25",
        LH: "4", FSH: "8", Glucose: "80", Cholesterol: "160"
      },
      moderate: {
        Age: "28", BMI: "26", Insulin: "15", Testosterone: "45",
        LH: "8", FSH: "6", Glucose: "95", Cholesterol: "190"
      },
      high: {
        Age: "30", BMI: "32", Insulin: "25", Testosterone: "70",
        LH: "18", FSH: "5", Glucose: "120", Cholesterol: "240"
      }
    };
    
    setFormData(sampleData[riskLevel]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="pcos-form-container">
      <div className="form-header">
        <h2>PCOS Risk Assessment</h2>
        <p>Enter your medical parameters to assess PCOS risk using AI prediction</p>
        
        {/* API Status Indicator */}
        <div className={`api-status ${apiStatus?.status}`}>
          <span className="status-dot"></span>
          API Status: {apiStatus?.status === "healthy" ? "Online" : "Offline"}
        </div>
      </div>

      <div className="form-content">
        {/* Sample Data Buttons */}
        <div className="sample-buttons">
  <h4>Try Sample Data:</h4>
  <div className="buttons-wrapper">
    <button
      type="button"
      onClick={() => fillSampleData('low')}
      className="sample-btn low"
    >
      Low Risk Profile
    </button>
    <button
      type="button"
      onClick={() => fillSampleData('moderate')}
      className="sample-btn moderate"
    >
      Moderate Risk Profile
    </button>
    <button
      type="button"
      onClick={() => fillSampleData('high')}
      className="sample-btn high"
    >
      High Risk Profile
    </button>
  </div>
</div>

        {/* <div className="sample-buttons">
          <h4>Try Sample Data:</h4>
          <button type="button" onClick={() => fillSampleData('low')} className="sample-btn low">
            Low Risk Profile
          </button>
          <button type="button" onClick={() => fillSampleData('moderate')} className="sample-btn moderate">
            Moderate Risk Profile
          </button>
          <button type="button" onClick={() => fillSampleData('high')} className="sample-btn high">
            High Risk Profile
          </button>
        </div> */}

        <form onSubmit={handleSubmit} className="pcos-form">
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="Age">Age (years)</label>
              <input
                type="number"
                id="Age"
                name="Age"
                value={formData.Age}
                onChange={handleChange}
                placeholder="e.g., 28"
                min="15"
                max="50"
                step="1"
              />
              <small>Typical range: 15-50 years</small>
            </div>

            <div className="form-group">
              <label htmlFor="BMI">BMI (kg/m²)</label>
              <input
                type="number"
                id="BMI"
                name="BMI"
                value={formData.BMI}
                onChange={handleChange}
                placeholder="e.g., 24.5"
                min="15"
                max="50"
                step="0.1"
              />
              <small>Typical range: 18-35</small>
            </div>

            <div className="form-group">
              <label htmlFor="Insulin">Insulin (μIU/mL)</label>
              <input
                type="number"
                id="Insulin"
                name="Insulin"
                value={formData.Insulin}
                onChange={handleChange}
                placeholder="e.g., 12"
                min="1"
                max="100"
                step="0.1"
              />
              <small>Typical range: 5-25</small>
            </div>

            <div className="form-group">
              <label htmlFor="Testosterone">Testosterone (ng/dL)</label>
              <input
                type="number"
                id="Testosterone"
                name="Testosterone"
                value={formData.Testosterone}
                onChange={handleChange}
                placeholder="e.g., 40"
                min="10"
                max="150"
                step="0.1"
              />
              <small>Typical range: 15-85</small>
            </div>

            <div className="form-group">
              <label htmlFor="LH">LH (mIU/mL)</label>
              <input
                type="number"
                id="LH"
                name="LH"
                value={formData.LH}
                onChange={handleChange}
                placeholder="e.g., 7"
                min="1"
                max="50"
                step="0.1"
              />
              <small>Luteinizing Hormone: 2-20</small>
            </div>

            <div className="form-group">
              <label htmlFor="FSH">FSH (mIU/mL)</label>
              <input
                type="number"
                id="FSH"
                name="FSH"
                value={formData.FSH}
                onChange={handleChange}
                placeholder="e.g., 6"
                min="1"
                max="30"
                step="0.1"
              />
              <small>Follicle Stimulating Hormone: 3-12</small>
            </div>

            <div className="form-group">
              <label htmlFor="Glucose">Glucose (mg/dL)</label>
              <input
                type="number"
                id="Glucose"
                name="Glucose"
                value={formData.Glucose}
                onChange={handleChange}
                placeholder="e.g., 90"
                min="50"
                max="300"
                step="1"
              />
              <small>Typical range: 70-140</small>
            </div>

            <div className="form-group">
              <label htmlFor="Cholesterol">Cholesterol (mg/dL)</label>
              <input
                type="number"
                id="Cholesterol"
                name="Cholesterol"
                value={formData.Cholesterol}
                onChange={handleChange}
                placeholder="e.g., 180"
                min="100"
                max="400"
                step="1"
              />
              <small>Typical range: 150-250</small>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading} className="predict-btn">
              {loading ? (
                <span>
                  <span className="spinner"></span>
                  Analyzing...
                </span>
              ) : (
                "Predict PCOS Risk"
              )}
            </button>
            <button type="button" onClick={resetForm} className="reset-btn">
              Reset Form
            </button>
          </div>
        </form>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className={`result-container ${result.risk_level?.toLowerCase()}`}>
            <h3>Prediction Results</h3>
            <div className="result-grid">
              <div className="result-item">
                <span className="label">Prediction:</span>
                <span className={`value ${result.pcos_risk ? 'positive' : 'negative'}`}>
                  {result.prediction_text}
                </span>
              </div>
              <div className="result-item">
                <span className="label">PCOS Probability:</span>
                <span className="value">{(result.probability * 100).toFixed(1)}%</span>
              </div>
              <div className="result-item">
                <span className="label">Risk Level:</span>
                <span className={`value risk-${result.risk_level?.toLowerCase()}`}>
                  {result.risk_level}
                </span>
              </div>
              <div className="result-item">
                <span className="label">Confidence:</span>
                <span className="value">{(result.confidence * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div className="probability-bar">
              <div className="bar-container">
                <div 
                  className="probability-fill"
                  style={{width: `${result.probability * 100}%`}}
                ></div>
              </div>
              <div className="bar-labels">
                <span>Healthy</span>
                <span>PCOS Risk</span>
              </div>
                {result && <Visualization result={result} />}
            </div>
          


            <div className="disclaimer">
              <p><strong>Disclaimer:</strong> This prediction is for educational purposes only and should not replace professional medical advice. Please consult with a healthcare provider for proper diagnosis and treatment.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

