import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import API_BASE_URL from '../config';
import './SymptomTracker.css';

const SymptomTracker = () => {
  const { token } = useAuth();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [flowIntensity, setFlowIntensity] = useState(2); // 0: None, 1: Light, 2: Medium, 3: Heavy
  const [symptoms, setSymptoms] = useState({
    acne: false,
    fatigue: false,
    moodChanges: false,
    bloating: false,
    foodCravings: false,
    hairFall: false,
    anxiety: false,
    headache: false
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  const getCurrentMonth = () => {
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'];
    return `${months[selectedDate.getMonth()]} ${selectedDate.getFullYear()}`;
  };

  const getDaysInMonth = () => {
    const year = selectedDate.getFullYear();
    const month = selectedDate.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    const days = [];
    // Previous month days
    for (let i = 0; i < firstDay; i++) {
      days.push({ day: '', current: false });
    }
    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ day: i, current: true });
    }
    
    return days;
  };

  const changeMonth = (direction) => {
    const newDate = new Date(selectedDate);
    newDate.setMonth(newDate.getMonth() + direction);
    setSelectedDate(newDate);
  };

  const handleSymptomToggle = (symptom) => {
    setSymptoms(prev => ({
      ...prev,
      [symptom]: !prev[symptom]
    }));
  };

  const handleSaveEntry = async () => {
    try {
      setSaving(true);
      setMessage(null);

      // Map symptoms to severity scores (0-3)
      const symptomData = {
        log_date: selectedDate.toISOString().split('T')[0], // Format: YYYY-MM-DD
        acne_severity: symptoms.acne ? 2 : 0,
        hirsutism_score: 0, // Not tracked in this UI
        hair_loss_score: symptoms.hairFall ? 2 : 0,
        fatigue_level: symptoms.fatigue ? 2 : 0,
        mood_swings: symptoms.moodChanges ? 2 : 0,
        anxiety_level: symptoms.anxiety ? 2 : 0,
        sleep_quality: 7, // Default value
        food_cravings: symptoms.foodCravings ? 2 : 0,
        bloating: symptoms.bloating ? 2 : 0,
        period_flow: getFlowLabel(),
        period_active: flowIntensity > 0
      };

      const response = await axios.post(
        `${API_BASE_URL}/lifestyle/save-symptom-log`,
        symptomData,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setMessage({ type: 'success', text: '✅ Entry saved successfully!' });
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setMessage(null);
      }, 3000);

    } catch (error) {
      console.error('Error saving entry:', error);
      setMessage({ 
        type: 'error', 
        text: '❌ Failed to save entry: ' + (error.response?.data?.error || error.message)
      });
    } finally {
      setSaving(false);
    }
  };

  const getFlowLabel = () => {
    const labels = ['None', 'Light', 'Medium', 'Heavy'];
    return labels[flowIntensity];
  };

  const symptomsList = [
    { id: 'acne', label: 'Acne', icon: '☀️' },
    { id: 'fatigue', label: 'Fatigue', icon: '😴' },
    { id: 'moodChanges', label: 'Mood Changes', icon: '🦋' },
    { id: 'bloating', label: 'Bloating', icon: '🎈' },
    { id: 'foodCravings', label: 'Food Cravings', icon: '💎' },
    { id: 'hairFall', label: 'Hair Fall', icon: '🎨' },
    { id: 'anxiety', label: 'Anxiety', icon: '😰' },
    { id: 'headache', label: 'Headache', icon: '🤕' }
  ];

  return (
    <div className="symptom-tracker-container">
      <div className="tracker-header">
        <h1>Symptom & Cycle Tracker</h1>
        <p>Track your daily symptoms and cycle to identify patterns</p>
      </div>

      <div className="tracker-content">
        {/* Calendar Section */}
        <div className="calendar-section">
          <div className="section-card">
            <h3>📅 Select Date</h3>
            <div className="calendar">
              <div className="calendar-header">
                <button onClick={() => changeMonth(-1)}>‹</button>
                <span>{getCurrentMonth()}</span>
                <button onClick={() => changeMonth(1)}>›</button>
              </div>
              <div className="calendar-weekdays">
                {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(day => (
                  <div key={day} className="weekday">{day}</div>
                ))}
              </div>
              <div className="calendar-days">
                {getDaysInMonth().map((item, index) => (
                  <div
                    key={index}
                    className={`calendar-day ${item.current ? 'current' : 'other'} ${
                      item.day === new Date().getDate() && 
                      selectedDate.getMonth() === new Date().getMonth() ? 'today' : ''
                    }`}
                  >
                    {item.day}
                  </div>
                ))}
              </div>
              <div className="calendar-legend">
                <div className="legend-item">
                  <span className="legend-dot period"></span>
                  <span>Period Days</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot ovulation"></span>
                  <span>Ovulation</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot fertile"></span>
                  <span>Fertile Window</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="right-section">
          {/* Period Flow Section */}
          <div className="section-card">
            <h3>🩸 Period Flow</h3>
            <div className="flow-section">
              <p className="flow-label">Flow Intensity: {getFlowLabel()}</p>
              <div className="flow-slider-container">
                <input
                  type="range"
                  min="0"
                  max="3"
                  value={flowIntensity}
                  onChange={(e) => setFlowIntensity(parseInt(e.target.value))}
                  className="flow-slider"
                />
                <div className="flow-labels">
                  <span>None</span>
                  <span>Light</span>
                  <span>Medium</span>
                  <span>Heavy</span>
                </div>
              </div>
            </div>
          </div>

          {/* Symptoms Section */}
          <div className="section-card">
            <h3>💚 Symptoms Today</h3>
            <div className="symptoms-grid">
              {symptomsList.map(symptom => (
                <div key={symptom.id} className="symptom-item">
                  <span className="symptom-icon">{symptom.icon}</span>
                  <span className="symptom-label">{symptom.label}</span>
                  <label className="toggle-switch">
                    <input
                      type="checkbox"
                      checked={symptoms[symptom.id]}
                      onChange={() => handleSymptomToggle(symptom.id)}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Message Display */}
          {message && (
            <div className={`message-box ${message.type}`}>
              {message.text}
            </div>
          )}

          {/* Save Button */}
          <button 
            className="save-button" 
            onClick={handleSaveEntry}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Today\'s Entry'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SymptomTracker;
