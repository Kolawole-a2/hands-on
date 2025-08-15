# Cognitive SOAR - Threat Attribution System

**From Prediction to Attribution: Intelligent Threat Analysis**

This project is an advanced Security Orchestration, Automation, and Response (SOAR) application that evolves beyond basic malicious/benign URL detection to provide intelligent threat actor attribution. Built with Python, PyCaret, and Streamlit, it represents the next generation of security analytics.

## 🎯 **Key Features**

### **Dual-Model Architecture**
- **Classification Model**: Advanced phishing URL detection using PyCaret's automated ML
- **Clustering Model**: Unsupervised learning for threat actor profile identification
- **Intelligent Attribution**: Maps technical indicators to three threat actor profiles

### **Threat Actor Profiles**
1. **🔴 Organized Cybercrime** - High-volume, financially motivated attacks
2. **🔵 State-Sponsored** - Sophisticated nation-state actors with strategic objectives  
3. **🟢 Hacktivist** - Ideologically motivated actors with mixed capabilities

### **Advanced Analytics**
- **Predictive Analytics**: Automated model training and comparison
- **Prescriptive Analytics**: GenAI-powered response plan generation
- **Visual Insights**: Feature importance and cluster visualization
- **Risk Scoring**: Dynamic risk contribution analysis

### **Technology Stack**
- **Machine Learning**: PyCaret for automated ML workflows
- **Web Interface**: Modern Streamlit application with responsive design
- **Containerization**: Docker and Docker Compose for deployment
- **AI Integration**: Google Gemini, OpenAI, and Grok support

## 🚀 **Quick Start**

### **Prerequisites**
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/) (optional but recommended)

### **1. Clone and Setup**
```bash
git clone <repository-url>
cd cognitive-soar
```

### **2. Configure API Keys**
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
GEMINI_API_KEY = "AIza..."
GROK_API_KEY = "gsk_..."
```

### **3. Launch Application**
```bash
make up
```
Access at: **[http://localhost:8501](http://localhost:8501)**

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   URL Features  │───▶│ Classification   │───▶│  Malicious?     │
│   (User Input)  │    │   Model         │    │   Yes/No        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Clustering     │───▶│ Threat Actor    │
                       │   Model         │    │   Profile       │
                       └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   GenAI         │───▶│ Response Plan   │
                       │   Integration   │    │   Generation    │
                       └──────────────────┘    └─────────────────┘
```

## 📊 **How It Works**

### **1. Feature Analysis**
The system analyzes 14 URL characteristics including:
- Technical indicators (SSL, IP usage, URL structure)
- Behavioral patterns (shortening services, subdomains)
- Sophistication metrics (political keywords, complexity levels)

### **2. Dual-Model Processing**
- **Classification**: Determines if URL is malicious (binary classification)
- **Clustering**: If malicious, identifies threat actor profile (3 clusters)

### **3. Threat Attribution**
Maps cluster IDs to threat actor profiles:
- **Cluster 0** → Organized Cybercrime
- **Cluster 1** → State-Sponsored  
- **Cluster 2** → Hacktivist

### **4. Response Generation**
Uses GenAI to create tailored incident response plans based on:
- Threat actor profile
- Technical indicators
- Risk assessment

## 🛠️ **Management Commands**

```bash
# Start the application
make up

# View logs
make logs

# Stop the application
make down

# Full cleanup (removes models and data)
make clean

# Rebuild containers
make build
```

## 📁 **Project Structure**

```
cognitive-soar/
├── README.md                 # This file
├── INSTALL.md               # Detailed installation guide
├── TESTING.md               # Testing procedures and test cases
├── Makefile                 # Build and deployment automation
├── docker-compose.yml       # Container orchestration
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── app.py                   # Main Streamlit application
├── train_model.py           # Model training and clustering
├── genai_prescriptions.py   # GenAI integration
├── .github/
│   └── workflows/
│       └── lint.yml         # GitHub Actions linting
└── models/                  # Trained models (auto-generated)
    ├── phishing_url_detector.pkl
    ├── threat_actor_profiler.pkl
    ├── feature_importance.png
    └── threat_clusters.png
```

## 🔬 **Technical Details**

### **Machine Learning Models**
- **Classification**: Random Forest, Extra Trees, LightGBM (auto-selected)
- **Clustering**: K-Means with 3 clusters (optimized for threat profiles)
- **Features**: 14 engineered URL characteristics
- **Training**: Automated with PyCaret's compare_models()

### **Data Generation**
- **Synthetic Dataset**: 1000 samples with realistic threat actor patterns
- **Balanced Classes**: 50% malicious, 50% benign
- **Threat Profiles**: Distinct feature distributions for each actor type

### **Performance Features**
- **Caching**: Streamlit resource caching for model loading
- **Async Processing**: Non-blocking UI during analysis
- **Error Handling**: Graceful degradation and user feedback

## 🧪 **Testing**

See [TESTING.md](TESTING.md) for comprehensive testing procedures including:
- Benign URL test cases
- Malicious URL tests for each threat actor profile
- Model validation procedures
- UI/UX testing scenarios

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Ensure code follows PEP8 standards
4. Add tests for new functionality
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- **PyCaret**: Automated machine learning framework
- **Streamlit**: Rapid web application development
- **scikit-learn**: Machine learning algorithms and utilities
- **Docker**: Containerization platform

---

**Cognitive SOAR System** - Advancing security analytics from prediction to intelligent attribution.
