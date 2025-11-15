import "./Education.css";
import "bootstrap/dist/css/bootstrap.min.css";

export default function Education() {
  return (
    <div className="container my-5 education-container">
      <h2 className="text-center mb-4">Understanding PCOS</h2>
      <p className="lead text-center">
        Polycystic Ovary Syndrome (PCOS) is a common hormonal disorder affecting
        women of reproductive age. It can impact menstrual cycles, fertility,
        metabolism, and appearance. Understanding the symptoms, causes, and
        management options is key to living a healthy life.
      </p>

      {/* Quick Facts */}
      <div className="card bg-light mb-4">
        <div className="card-body">
          <h4 className="card-title">💡 Did You Know?</h4>
          <ul className="list-group list-group-flush">
            <li className="list-group-item">1 in 10 women of reproductive age may have PCOS.</li>
            <li className="list-group-item">Early diagnosis can help prevent long-term health issues.</li>
            <li className="list-group-item">PCOS can affect mental health, including anxiety and depression.</li>
          </ul>
        </div>
      </div>

      {/* Main Sections */}
      <div className="row">
        <div className="col-md-6 mb-4">
          <div className="card h-100">
            <div className="card-body">
              <h4 className="card-title">Symptoms</h4>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">Irregular or absent periods</li>
                <li className="list-group-item">Excess hair growth (hirsutism)</li>
                <li className="list-group-item">Acne or oily skin</li>
                <li className="list-group-item">Thinning hair or hair loss</li>
                <li className="list-group-item">Weight gain or difficulty losing weight</li>
                <li className="list-group-item">Fatigue or low energy</li>
                <li className="list-group-item">Mood swings or depression</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card h-100">
            <div className="card-body">
              <h4 className="card-title">Causes & Risk Factors</h4>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">Genetic factors (family history)</li>
                <li className="list-group-item">Insulin resistance and high insulin levels</li>
                <li className="list-group-item">Hormonal imbalances (high androgens)</li>
                <li className="list-group-item">Obesity or sedentary lifestyle</li>
                <li className="list-group-item">Chronic inflammation</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-12 mb-4">
          <div className="card h-100">
            <div className="card-body">
              <h4 className="card-title">Management & Treatment</h4>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">Maintain a balanced diet low in refined carbs</li>
                <li className="list-group-item">Exercise regularly (30–60 mins, 3–5 times/week)</li>
                <li className="list-group-item">Weight management for hormonal balance</li>
                <li className="list-group-item">Medications: hormonal therapy, insulin-sensitizers</li>
                <li className="list-group-item">Fertility treatments if planning pregnancy</li>
                <li className="list-group-item">Track symptoms and consult healthcare provider</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Lifestyle Tips */}
      <div className="card bg-light mb-4">
        <div className="card-body">
          <h4 className="card-title">🌿 Tips for a Healthy Lifestyle</h4>
          <ul className="list-group list-group-flush">
            <li className="list-group-item">Follow a low-glycemic index (GI) diet</li>
            <li className="list-group-item">Exercise regularly (a mix of cardio + strength)</li>
            <li className="list-group-item">Manage stress through yoga, meditation, or hobbies</li>
            <li className="list-group-item">Sleep 7–8 hours nightly</li>
            <li className="list-group-item">Track symptoms with apps or journals</li>
          </ul>
        </div>
      </div>

      {/* Risk Awareness */}
      <div className="alert alert-info text-center">
        <h5>Why Knowing Your Risk Matters</h5>
        <p>
          Early detection of PCOS symptoms and risk factors can help prevent
          long-term complications like diabetes, heart disease, and infertility.
          Use the <strong>PCOS Risk Predictor</strong> to understand your profile
          and take proactive steps for your health.
        </p>
      </div>

      {/* References */}
      <div className="card bg-light mb-4">
        <div className="card-body">
          <h4 className="card-title">References & Resources</h4>
          <ul>
            <li>
              <a href="https://www.womenshealth.gov/a-z-topics/polycystic-ovary-syndrome" target="_blank" rel="noreferrer">
                WomensHealth.gov: PCOS Overview
              </a>
            </li>
            <li>
              <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3489732/" target="_blank" rel="noreferrer">
                NCBI: PCOS Research Article
              </a>
            </li>
            <li>
              <a href="https://www.mayoclinic.org/diseases-conditions/pcos/symptoms-causes/syc-20353439" target="_blank" rel="noreferrer">
                Mayo Clinic: PCOS Symptoms & Causes
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
