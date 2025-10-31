"""
Lifestyle-based PCOS Risk Prediction Model
Uses self-reported symptoms and lifestyle data (no lab tests required)
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

# Sample data creation (in real scenario, this would come from dataset)
def create_sample_pcos_data(n_samples=1000):
    """
    Create synthetic PCOS data based on known correlations
    In production, replace with real Kaggle dataset
    """
    np.random.seed(42)
    
    data = []
    for i in range(n_samples):
        # PCOS status (target)
        has_pcos = np.random.choice([0, 1], p=[0.7, 0.3])  # 30% PCOS prevalence
        
        # Features with different distributions based on PCOS status
        if has_pcos:
            age = np.random.normal(28, 5)
            bmi = np.random.normal(28, 5)  # Higher BMI in PCOS
            cycle_regularity = np.random.choice([0, 1, 2], p=[0.1, 0.2, 0.7])  # Mostly irregular
            cycle_length = np.random.normal(45, 15)  # Longer cycles
            hirsutism = np.random.choice([0, 1, 2, 3], p=[0.2, 0.2, 0.3, 0.3])  # More hair growth
            acne = np.random.choice([0, 1, 2, 3], p=[0.2, 0.3, 0.3, 0.2])
            hair_loss = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])
            weight_gain_difficulty = np.random.choice([0, 1, 2], p=[0.2, 0.3, 0.5])
            family_history = np.random.choice([0, 1], p=[0.4, 0.6])
            stress_level = np.random.normal(7, 2)
            exercise_frequency = np.random.normal(2, 1)  # Less exercise
            sleep_quality = np.random.normal(4, 2)  # Worse sleep
        else:
            age = np.random.normal(28, 5)
            bmi = np.random.normal(23, 3)  # Normal BMI
            cycle_regularity = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Mostly regular
            cycle_length = np.random.normal(28, 3)  # Normal cycles
            hirsutism = np.random.choice([0, 1, 2, 3], p=[0.6, 0.3, 0.1, 0.0])
            acne = np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.2, 0.0])
            hair_loss = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])
            weight_gain_difficulty = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])
            family_history = np.random.choice([0, 1], p=[0.7, 0.3])
            stress_level = np.random.normal(5, 2)
            exercise_frequency = np.random.normal(3, 1)
            sleep_quality = np.random.normal(7, 2)
        
        # Clip values to valid ranges
        age = np.clip(age, 18, 45)
        bmi = np.clip(bmi, 15, 45)
        cycle_length = np.clip(cycle_length, 20, 90)
        stress_level = np.clip(stress_level, 0, 10)
        exercise_frequency = np.clip(exercise_frequency, 0, 7)
        sleep_quality = np.clip(sleep_quality, 0, 10)
        
        data.append({
            'Age': age,
            'BMI': bmi,
            'CycleRegularity': cycle_regularity,  # 0=Regular, 1=Irregular, 2=VeryIrregular
            'CycleLength': cycle_length,
            'Hirsutism': hirsutism,  # 0-3 scale
            'Acne': acne,  # 0-3 scale
            'HairLoss': hair_loss,  # 0-2 scale
            'WeightGainDifficulty': weight_gain_difficulty,  # 0-2 scale
            'FamilyHistory': family_history,
            'StressLevel': stress_level,
            'ExerciseFrequency': exercise_frequency,
            'SleepQuality': sleep_quality,
            'PCOS': has_pcos
        })
    
    return pd.DataFrame(data)


def train_lifestyle_model():
    """Train the lifestyle-based PCOS prediction model"""
    print("🚀 Training Lifestyle-based PCOS Prediction Model...")
    print("=" * 60)
    
    # Create/load data
    print("\n📊 Creating dataset...")
    df = create_sample_pcos_data(n_samples=2000)
    
    print(f"Dataset size: {len(df)} samples")
    print(f"PCOS cases: {df['PCOS'].sum()} ({df['PCOS'].mean()*100:.1f}%)")
    print(f"Healthy cases: {(1-df['PCOS']).sum()} ({(1-df['PCOS']).mean()*100:.1f}%)")
    
    # Features and target
    feature_names = [
        'Age', 'BMI', 'CycleRegularity', 'CycleLength', 
        'Hirsutism', 'Acne', 'HairLoss', 'WeightGainDifficulty',
        'FamilyHistory', 'StressLevel', 'ExerciseFrequency', 'SleepQuality'
    ]
    
    X = df[feature_names]
    y = df['PCOS']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📈 Training set: {len(X_train)} samples")
    print(f"📉 Test set: {len(X_test)} samples")
    
    # Scale features
    print("\n⚙️ Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("\n🌲 Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\n✅ Model Training Complete!")
    print("=" * 60)
    
    # Training accuracy
    train_pred = model.predict(X_train_scaled)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"\n📊 Training Accuracy: {train_accuracy*100:.2f}%")
    
    # Test accuracy
    test_pred = model.predict(X_test_scaled)
    test_accuracy = accuracy_score(y_test, test_pred)
    print(f"📊 Test Accuracy: {test_accuracy*100:.2f}%")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    print(f"📊 Cross-Validation Accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
    
    # Classification report
    print("\n📋 Classification Report:")
    print(classification_report(y_test, test_pred, target_names=['Healthy', 'PCOS']))
    
    # Feature importance
    print("\n🔍 Feature Importance:")
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        print(f"  {row['Feature']:25s}: {row['Importance']:.4f}")
    
    # Save model, scaler, and feature names
    print("\n💾 Saving model files...")
    joblib.dump(model, 'lifestyle_pcos_model.pkl')
    joblib.dump(scaler, 'lifestyle_scaler.pkl')
    joblib.dump(feature_names, 'lifestyle_features.pkl')
    
    print("\n✅ Model saved successfully!")
    print("   - lifestyle_pcos_model.pkl")
    print("   - lifestyle_scaler.pkl")
    print("   - lifestyle_features.pkl")
    
    # Test prediction
    print("\n🧪 Testing sample predictions...")
    test_sample_predictions(model, scaler, feature_names)
    
    return model, scaler, feature_names


def test_sample_predictions(model, scaler, feature_names):
    """Test the model with sample data"""
    
    # Sample 1: High risk profile
    high_risk = pd.DataFrame([{
        'Age': 30,
        'BMI': 32,
        'CycleRegularity': 2,  # Very irregular
        'CycleLength': 60,
        'Hirsutism': 3,  # Severe
        'Acne': 2,
        'HairLoss': 2,
        'WeightGainDifficulty': 2,
        'FamilyHistory': 1,
        'StressLevel': 8,
        'ExerciseFrequency': 1,
        'SleepQuality': 4
    }])
    
    # Sample 2: Low risk profile
    low_risk = pd.DataFrame([{
        'Age': 25,
        'BMI': 22,
        'CycleRegularity': 0,  # Regular
        'CycleLength': 28,
        'Hirsutism': 0,
        'Acne': 0,
        'HairLoss': 0,
        'WeightGainDifficulty': 0,
        'FamilyHistory': 0,
        'StressLevel': 3,
        'ExerciseFrequency': 5,
        'SleepQuality': 8
    }])
    
    for profile_name, profile_data in [('High Risk', high_risk), ('Low Risk', low_risk)]:
        X_scaled = scaler.transform(profile_data[feature_names])
        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0]
        
        print(f"\n  {profile_name} Profile:")
        print(f"    Prediction: {'PCOS Risk' if prediction == 1 else 'Healthy'}")
        print(f"    PCOS Probability: {probability[1]*100:.1f}%")
        print(f"    Healthy Probability: {probability[0]*100:.1f}%")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  LIFESTYLE-BASED PCOS PREDICTION MODEL TRAINING")
    print("="*60 + "\n")
    
    model, scaler, features = train_lifestyle_model()
    
    print("\n" + "="*60)
    print("  🎉 TRAINING COMPLETE!")
    print("="*60 + "\n")
