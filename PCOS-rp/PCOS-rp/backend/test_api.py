import requests
import json

def test_api():
    """Test the PCOS prediction API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing PCOS Prediction API")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API not running. Please start the Flask app first.")
        return
    
    # Test 2: Get features
    print("\n2️⃣ Getting feature information...")
    try:
        response = requests.get(f"{base_url}/features")
        features_info = response.json()
        print(f"Features: {features_info['features']}")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Test 3: Make predictions with different risk profiles
    test_cases = [
        {
            "name": "Low Risk Patient",
            "data": {
                "Age": 25, "BMI": 21, "Insulin": 8, "Testosterone": 25,
                "LH": 4, "FSH": 8, "Glucose": 80, "Cholesterol": 160
            }
        },
        {
            "name": "Moderate Risk Patient",
            "data": {
                "Age": 28, "BMI": 26, "Insulin": 15, "Testosterone": 45,
                "LH": 8, "FSH": 6, "Glucose": 95, "Cholesterol": 190
            }
        },
        {
            "name": "High Risk Patient",
            "data": {
                "Age": 30, "BMI": 32, "Insulin": 25, "Testosterone": 70,
                "LH": 18, "FSH": 5, "Glucose": 120, "Cholesterol": 240
            }
        }
    ]
    
    print("\n3️⃣ Testing predictions...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test Case {i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"    Prediction: {result['prediction_text']}")
                print(f"    PCOS Probability: {result['probability']:.1%}")
                print(f"    Risk Level: {result['risk_level']}")
                print(f"    Confidence: {result['confidence']:.3f}")
            else:
                print(f"    Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    # Test 4: Test error handling
    print("\n4️⃣ Testing error handling...")
    try:
        # Missing required field
        incomplete_data = {"Age": 25, "BMI": 21}
        response = requests.post(
            f"{base_url}/predict",
            json=incomplete_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Incomplete data test - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Expected error response: {response.json()}")
    except Exception as e:
        print(f"Error handling test failed: {e}")
    
    print("\n✅ API testing complete!")

if __name__ == "__main__":
    test_api()
