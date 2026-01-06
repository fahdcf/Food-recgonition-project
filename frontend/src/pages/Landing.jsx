import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import './Landing.css';

export const Landing = () => {
  const { stats } = useAppContext();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: 'fas fa-search',
      title: 'AI-Powered Recognition',
      description: 'Advanced deep learning identifies 110+ dishes with 85%+ accuracy',
    },
    {
      icon: 'fas fa-chart-pie',
      title: 'Nutritional Insights',
      description: 'Instant macro breakdown - calories, protein, carbs, and fats',
    },
    {
      icon: 'fas fa-utensils',
      title: 'Recipe Library',
      description: 'Step-by-step cooking instructions for every dish',
    },
    {
      icon: 'fas fa-mobile-alt',
      title: 'Meal Tracking',
      description: 'Log meals and monitor daily nutrition goals effortlessly',
    },
  ];

  const stats_data = [
    { value: '110+', label: 'Food Classes' },
    { value: '174', label: 'Dish Database' },
    { value: '85%', label: 'Accuracy' },
    { value: '0.3s', label: 'Prediction Speed' },
  ];

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className={`hero-text ${isVisible ? 'fade-in' : ''}`}>
            <div className="hero-badge">
              <span className="badge-dot"></span>
              <span>Powered by ResNet50 + Logistic Regression</span>
            </div>
            <h1 className="hero-title">
              Identify Your Food
              <br />
              <span className="gradient-text">Track Your Health</span>
            </h1>
            <p className="hero-description">
              Upload any food image and get instant AI predictions with nutritional breakdowns, 
              recipes, and personalized meal tracking. Transform how you understand your diet.
            </p>
            <div className="hero-cta">
              <Link to="/upload" className="btn-primary">
                <span>Start Recognition</span>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M6 3L11 8L6 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </Link>
              <Link to="/dishes" className="btn-secondary">
                Browse 174 Dishes
              </Link>
            </div>
          </div>

          <div className={`hero-visual ${isVisible ? 'slide-in' : ''}`}>
            <div className="visual-card glass-card">
              <div className="scan-frame">
                <div className="scan-line"></div>
                <div className="scan-corners"></div>
                <div className="placeholder-image">
                  <img src="/couscous_15.png" alt="AI Recognition Demo - Couscous" className="demo-food-image" />
                </div>
              </div>
              <div className="prediction-demo">
                <div className="demo-result">
                  <div className="demo-confidence">
                    <span className="confidence-label">Top Match</span>
                    <span className="confidence-value">94.3%</span>
                  </div>
                  <div className="demo-dish">Pizza Margherita</div>
                  <div className="demo-bar">
                    <div className="demo-fill" style={{width: '94.3%'}}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-grid">
          {stats_data.map((stat, idx) => (
            <div key={idx} className="stat-card glass-card">
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <h2 className="section-title">Powerful Features</h2>
          <p className="section-description">
            Everything you need to identify, track, and understand your food
          </p>
        </div>
        <div className="features-grid">
          {features.map((feature, idx) => (
            <div key={idx} className="feature-card glass-card">
              <div className="feature-icon"><i className={feature.icon}></i></div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="workflow-section">
        <div className="section-header">
          <h2 className="section-title">How It Works</h2>
          <p className="section-description">Three simple steps to food recognition</p>
        </div>
        <div className="workflow-steps">
          <div className="workflow-step">
            <div className="step-number">1</div>
            <div className="step-icon"><i className="fas fa-cloud-upload-alt"></i></div>
            <h3 className="step-title">Upload Image</h3>
            <p className="step-description">
              Take a photo or upload from your device
            </p>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">2</div>
            <div className="step-icon"><i className="fas fa-brain"></i></div>
            <h3 className="step-title">AI Analysis</h3>
            <p className="step-description">
              Our model identifies the dish in milliseconds
            </p>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">3</div>
            <div className="step-icon"><i className="fas fa-chart-bar"></i></div>
            <h3 className="step-title">Get Results</h3>
            <p className="step-description">
              View nutrition, recipes, and track your meal
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-card glass-card">
          <h2 className="cta-title">Ready to get started?</h2>
          <p className="cta-description">
            Join thousands tracking their nutrition with AI-powered food recognition
          </p>
          <Link to="/upload" className="btn-primary btn-large">
            <span>Try It Now</span>
            <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
              <path d="M6 3L11 8L6 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </div>
      </section>
    </div>
  );
};