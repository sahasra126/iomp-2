import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import API_BASE_URL from '../config';
import './LifestyleAssessment.css';

const LifestyleAssessment = () => {
  const { token } = useAuth();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Debug: Log when step changes
  React.useEffect(() => {
    console.log('Step changed to:', step);
  }, [step]);

  // Debug: Log when component mounts/unmounts
  React.useEffect(() => {
    console.log('LifestyleAssessment component mounted');
    return () => {
      console.log('LifestyleAssessment component unmounting!');
    };
  }, []);

  const [formData, setFormData] = useState({
    // Basic Info
    Age: '',
    height: '',
    weight: '',
    BMI: '',
    
    // Cycle Info
    CycleRegularity: '0',
    CycleLength: '',
    
    // Physical Symptoms
    Hirsutism: '0',
    Acne: '0',
    HairLoss: '0',
    WeightGainDifficulty: '0',
    
    // Lifestyle
    StressLevel: '5',
    ExerciseFrequency: '3',
    SleepQuality: '7',
    
    // Family History
    FamilyHistory: '0'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    let newData = { ...formData, [name]: value };
    
    // Auto-calculate BMI
    if (name === 'height' || name === 'weight') {
      if (newData.height && newData.weight) {
        const heightM = parseFloat(newData.height) / 100;
        const bmi = (parseFloat(newData.weight) / (heightM * heightM)).toFixed(1);
        newData.BMI = bmi;
      }
    }
    
    setFormData(newData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Final validation before submission
    if (!formData.Age || !formData.height || !formData.weight || !formData.CycleLength) {
      setError('Please complete all required fields in Basic Info (Step 1)');
      setStep(1);
      return;
    }
    
    setLoading(true);
    setError(null);

    try {
      const assessmentData = {
        Age: parseFloat(formData.Age),
        BMI: parseFloat(formData.BMI),
        CycleRegularity: parseInt(formData.CycleRegularity),
        CycleLength: parseFloat(formData.CycleLength),
        Hirsutism: parseInt(formData.Hirsutism),
        Acne: parseInt(formData.Acne),
        HairLoss: parseInt(formData.HairLoss),
        WeightGainDifficulty: parseInt(formData.WeightGainDifficulty),
        FamilyHistory: parseInt(formData.FamilyHistory),
        StressLevel: parseFloat(formData.StressLevel),
        ExerciseFrequency: parseFloat(formData.ExerciseFrequency),
        SleepQuality: parseFloat(formData.SleepQuality),
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight)
      };

      const response = await axios.post(
        `${API_BASE_URL}/lifestyle/assess`,
        assessmentData,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setResult(response.data);
      setStep(4); // Move to results step
    } catch (err) {
      setError(err.response?.data?.error || 'Assessment failed. Please try again.');
      console.error('Assessment error:', err);
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    console.log('nextStep called, current step:', step);
    
    // Validate current step before moving forward
    if (step === 1) {
      if (!formData.Age || !formData.height || !formData.weight || !formData.CycleLength) {
        setError('Please fill in all required fields in Basic Info');
        return;
      }
    }
    // Step 2 has all dropdown fields with default values, so no validation needed
    // Step 3 is the last step, so nextStep shouldn't be called from there
    
    setError(null);
    const newStep = step + 1;
    console.log('Moving to step:', newStep);
    setStep(newStep);
  };

  const prevStep = () => {
    if (step > 1) {
      setError(null);
      setStep(step - 1);
    }
  };

  const resetAssessment = () => {
    setStep(1);
    setResult(null);
    setError(null);
  };

  return (
    <div className="lifestyle-assessment-container">
      <div className="assessment-header">
        <h1>Lifestyle-Based PCOS Assessment</h1>
        <p>Answer questions about your symptoms and lifestyle - no blood tests required!</p>
        <div style={{fontSize: '12px', color: '#666', marginTop: '10px'}}>
          DEBUG: Current Step = {step}
        </div>
      </div>

      {!result && (
        <div className="progress-bar">
          <div className="progress-steps">
            {[1, 2, 3].map(num => (
              <div key={num} className={`progress-step ${step >= num ? 'active' : ''}`}>
                <div className="step-circle">{num}</div>
                <div className="step-label">
                  {num === 1 ? 'Basic Info' : num === 2 ? 'Symptoms' : 'Lifestyle'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="assessment-content">
        {!result ? (
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              console.log('Form submit called, step:', step);
              if (step !== 3) {
                console.log('Form submission prevented - not on final step');
                return false;
              }
              handleSubmit(e);
            }}
            className="assessment-form"
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                console.log('Enter key pressed, preventing default');
                e.preventDefault();
                if (step < 3) {
                  nextStep();
                }
              }
            }}
          >
            {/* Step 1: Basic Info */}
            {step === 1 && (
              <div className="form-step" data-step="1">
                <h2>📋 Basic Information</h2>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Age *</label>
                    <input
                      type="number"
                      name="Age"
                      value={formData.Age}
                      onChange={handleChange}
                      placeholder="e.g., 28"
                      min="15"
                      max="50"
                    />
                  </div>

                  <div className="form-group">
                    <label>Height (cm) *</label>
                    <input
                      type="number"
                      name="height"
                      value={formData.height}
                      onChange={handleChange}
                      placeholder="e.g., 165"
                      min="120"
                      max="220"
                    />
                  </div>

                  <div className="form-group">
                    <label>Weight (kg) *</label>
                    <input
                      type="number"
                      name="weight"
                      value={formData.weight}
                      onChange={handleChange}
                      placeholder="e.g., 65"
                      min="30"
                      max="200"
                    />
                  </div>

                  <div className="form-group">
                    <label>BMI (calculated)</label>
                    <input
                      type="text"
                      name="BMI"
                      value={formData.BMI}
                      readOnly
                      placeholder="Auto-calculated"
                      className="readonly"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group full-width">
                    <label>Menstrual Cycle Regularity *</label>
                    <select
                      name="CycleRegularity"
                      value={formData.CycleRegularity}
                      onChange={handleChange}
                    >
                      <option value="0">Regular (consistent cycles)</option>
                      <option value="1">Irregular (varies by more than 7 days)</option>
                      <option value="2">Very Irregular (unpredictable or absent periods)</option>
                    </select>
                  </div>

                  <div className="form-group full-width">
                    <label>Average Cycle Length (days) *</label>
                    <input
                      type="number"
                      name="CycleLength"
                      value={formData.CycleLength}
                      onChange={handleChange}
                      placeholder="e.g., 28"
                      min="20"
                      max="90"
                    />
                    <small>Normal range: 21-35 days</small>
                  </div>
                </div>

                <div className="form-group full-width">
                  <label>Family History of PCOS *</label>
                  <div className="radio-group">
                    <label>
                      <input
                        type="radio"
                        name="FamilyHistory"
                        value="0"
                        checked={formData.FamilyHistory === '0'}
                        onChange={handleChange}
                      />
                      <span>No known family history</span>
                    </label>
                    <label>
                      <input
                        type="radio"
                        name="FamilyHistory"
                        value="1"
                        checked={formData.FamilyHistory === '1'}
                        onChange={handleChange}
                      />
                      <span>Mother, sister, or aunt has PCOS</span>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Symptoms */}
            {step === 2 && (
              <div className="form-step" data-step="2">
                <h2>🩺 Physical Symptoms</h2>
                
                <div className="form-group full-width">
                  <label>Excessive Hair Growth (Hirsutism) *</label>
                  <select
                    name="Hirsutism"
                    value={formData.Hirsutism}
                    onChange={handleChange}
                  >
                    <option value="0">None - No excess hair</option>
                    <option value="1">Mild - Slight excess on face or body</option>
                    <option value="2">Moderate - Noticeable facial or body hair</option>
                    <option value="3">Severe - Significant excess hair growth</option>
                  </select>
                </div>

                <div className="form-group full-width">
                  <label>Acne Severity *</label>
                  <select
                    name="Acne"
                    value={formData.Acne}
                    onChange={handleChange}
                  >
                    <option value="0">None - Clear skin</option>
                    <option value="1">Mild - Occasional breakouts</option>
                    <option value="2">Moderate - Regular acne, some scarring</option>
                    <option value="3">Severe - Persistent cystic acne</option>
                  </select>
                </div>

                <div className="form-group full-width">
                  <label>Hair Thinning/Loss (Scalp) *</label>
                  <select
                    name="HairLoss"
                    value={formData.HairLoss}
                    onChange={handleChange}
                  >
                    <option value="0">None - Normal hair thickness</option>
                    <option value="1">Mild - Slight thinning noticed</option>
                    <option value="2">Moderate to Severe - Significant hair loss</option>
                  </select>
                </div>

                <div className="form-group full-width">
                  <label>Weight Management *</label>
                  <select
                    name="WeightGainDifficulty"
                    value={formData.WeightGainDifficulty}
                    onChange={handleChange}
                  >
                    <option value="0">Easy to maintain/lose weight</option>
                    <option value="1">Somewhat difficult to lose weight</option>
                    <option value="2">Very difficult to lose weight despite efforts</option>
                  </select>
                </div>
              </div>
            )}

            {/* Step 3: Lifestyle */}
            {step === 3 && (
              <div className="form-step" data-step="3">
                <h2>🏃‍♀️ Lifestyle Factors</h2>
                
                <div className="form-group full-width">
                  <label>Exercise Frequency (days per week) *</label>
                  <input
                    type="range"
                    name="ExerciseFrequency"
                    value={formData.ExerciseFrequency}
                    onChange={handleChange}
                    min="0"
                    max="7"
                    step="1"
                  />
                  <div className="range-value">{formData.ExerciseFrequency} days/week</div>
                  <small>30+ minutes of moderate activity</small>
                </div>

                <div className="form-group full-width">
                  <label>Sleep Quality (0-10) *</label>
                  <input
                    type="range"
                    name="SleepQuality"
                    value={formData.SleepQuality}
                    onChange={handleChange}
                    min="0"
                    max="10"
                    step="1"
                  />
                  <div className="range-value">{formData.SleepQuality}/10</div>
                  <small>0 = Poor sleep, 10 = Excellent sleep</small>
                </div>

                <div className="form-group full-width">
                  <label>Stress Level (0-10) *</label>
                  <input
                    type="range"
                    name="StressLevel"
                    value={formData.StressLevel}
                    onChange={handleChange}
                    min="0"
                    max="10"
                    step="1"
                  />
                  <div className="range-value">{formData.StressLevel}/10</div>
                  <small>0 = No stress, 10 = Extremely stressed</small>
                </div>
              </div>
            )}

            {error && (
              <div className="error-message">{error}</div>
            )}

            <div className="form-actions">
              {step > 1 && (
                <button type="button" onClick={prevStep} className="btn-secondary">
                  ← Previous
                </button>
              )}
              {step < 3 ? (
                <button type="button" onClick={nextStep} className="btn-primary">
                  Next →
                </button>
              ) : step === 3 ? (
                <button 
                  type="button" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleSubmit(e);
                  }}
                  disabled={loading} 
                  className="btn-submit"
                >
                  {loading ? 'Analyzing...' : 'Get My Risk Assessment'}
                </button>
              ) : null}
            </div>
          </form>
        ) : (
          <div className="assessment-results">
            <div className={`risk-badge ${result.risk_level.toLowerCase()}`}>
              <div className="risk-icon">
                {result.risk_level === 'Low' ? '✅' : result.risk_level === 'Moderate' ? '⚠️' : '🚨'}
              </div>
              <div className="risk-info">
                <h2>{result.risk_level} Risk</h2>
                <p>{result.prediction_text}</p>
              </div>
            </div>

            <div className="result-stats">
              <div className="stat">
                <div className="stat-value">{(result.probability * 100).toFixed(1)}%</div>
                <div className="stat-label">PCOS Probability</div>
              </div>
              <div className="stat">
                <div className="stat-value">{(result.confidence * 100).toFixed(1)}%</div>
                <div className="stat-label">Model Confidence</div>
              </div>
            </div>

            <div className="recommendations-section">
              <h3>📋 Personalized Recommendations</h3>
              {result.recommendations && result.recommendations.map((rec, index) => (
                <div key={index} className={`recommendation-card priority-${rec.priority}`}>
                  <div className="rec-header">
                    <span className="rec-category">{rec.category}</span>
                    <span className={`rec-priority ${rec.priority}`}>{rec.priority}</span>
                  </div>
                  <h4>{rec.title}</h4>
                  <p>{rec.description}</p>
                  <ul className="rec-actions">
                    {rec.actions.map((action, i) => (
                      <li key={i}>{action}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div className="result-actions">
              <button onClick={resetAssessment} className="btn-secondary">
                Take Another Assessment
              </button>
              <button onClick={() => window.location.href = '/dashboard'} className="btn-primary">
                View Dashboard
              </button>
            </div>

            <div className="disclaimer">
              <p><strong>⚠️ Important:</strong> This assessment is for educational purposes only and does not replace professional medical diagnosis. If you're concerned about PCOS, please consult a healthcare provider for proper testing and diagnosis.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LifestyleAssessment;
