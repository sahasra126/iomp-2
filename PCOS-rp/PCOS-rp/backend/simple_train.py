#!/usr/bin/env python3

print("🚀 Starting PCOS Model Training...")

try:
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, roc_auc_score
    import joblib
    
    print("✅ All libraries imported successfully")
    
    # Generate synthetic data
    print("📊 Generating synthetic PCOS data...")
    np.random.seed(42)
    
    # Create 1000 samples
    n_samples = 1000
    n_healthy = int(n_samples * 0.7)
    n_pcos = n_samples - n_healthy
    
    # Healthy samples
    healthy_data = np.column_stack([
        np.random.normal(28, 6, n_healthy),      # Age
        np.random.normal(23, 3, n_healthy),      # BMI
        np.random.normal(12, 4, n_healthy),      # Insulin
        np.random.normal(35, 10, n_healthy),     # Testosterone
        np.random.normal(6, 2, n_healthy),       # LH
        np.random.normal(7, 2, n_healthy),       # FSH
        np.random.normal(90, 10, n_healthy),     # Glucose
        np.random.normal(180, 30, n_healthy),    # Cholesterol
    ])
    healthy_labels = np.zeros(n_healthy)
    
    # PCOS samples
    pcos_data = np.column_stack([
        np.random.normal(26, 5, n_pcos),         # Age
        np.random.normal(28, 5, n_pcos),         # BMI
        np.random.normal(18, 6, n_pcos),         # Insulin
        np.random.normal(55, 15, n_pcos),        # Testosterone
        np.random.normal(12, 4, n_pcos),         # LH
        np.random.normal(6, 2, n_pcos),          # FSH
        np.random.normal(105, 15, n_pcos),       # Glucose
        np.random.normal(200, 40, n_pcos),       # Cholesterol
    ])
    pcos_labels = np.ones(n_pcos)
    
    # Combine data
    X = np.vstack([healthy_data, pcos_data])
    y = np.concatenate([healthy_labels, pcos_labels])
    feature_names = ['Age', 'BMI', 'Insulin', 'Testosterone', 'LH', 'FSH', 'Glucose', 'Cholesterol']
    
    print(f"✅ Dataset created: {X.shape}, PCOS cases: {np.sum(y)} ({np.mean(y)*100:.1f}%)")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✅ Data preprocessing complete")
    
    # Train models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    print("\n🔄 Training and comparing models...")
    
    for name, model in models.items():
        print(f"\n  Training {name}...")
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
        
        # Train on full training set
        model.fit(X_train_scaled, y_train)
        
        # Test predictions
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"    CV ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        print(f"    Test Accuracy: {accuracy:.3f}")
        print(f"    Test ROC-AUC: {roc_auc:.3f}")
        
        if roc_auc > best_score:
            best_score = roc_auc
            best_model = model
            best_name = name
    
    print(f"\n🏆 Best Model: {best_name}")
    print(f"🎯 Best ROC-AUC Score: {best_score:.3f}")
    
    # Save the best model
    print(f"\n💾 Saving {best_name}...")
    joblib.dump(best_model, "pcos_model.pkl")
    joblib.dump(scaler, "pcos_scaler.pkl")
    joblib.dump(feature_names, "feature_names.pkl")
    
    print("✅ Model training complete!")
    print(f"📁 Files saved: pcos_model.pkl, pcos_scaler.pkl, feature_names.pkl")
    
    # Quick test
    print(f"\n🧪 Quick test:")
    sample = np.array([[25, 22, 10, 30, 5, 7, 85, 170]])
    sample_scaled = scaler.transform(sample)
    pred = best_model.predict(sample_scaled)[0]
    prob = best_model.predict_proba(sample_scaled)[0, 1]
    print(f"Sample prediction: {'PCOS' if pred == 1 else 'Healthy'} (probability: {prob:.3f})")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
