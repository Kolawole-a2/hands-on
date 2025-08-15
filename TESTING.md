# Testing Guide - Cognitive SOAR System

This document provides comprehensive testing procedures and test cases for validating the Cognitive SOAR Threat Attribution System.

## 🧪 **Testing Overview**

### **Testing Objectives**
- Validate URL classification accuracy
- Verify threat actor attribution functionality
- Test GenAI integration and response generation
- Ensure UI/UX functionality across different scenarios
- Validate model training and persistence

### **Testing Levels**
1. **Unit Testing**: Individual component validation
2. **Integration Testing**: Component interaction testing
3. **System Testing**: End-to-end workflow validation
4. **User Acceptance Testing**: Real-world scenario validation

## 🚀 **Pre-Testing Setup**

### **Environment Preparation**
```bash
# Ensure clean environment
make clean

# Build and start application
make up

# Wait for models to train (check logs)
make logs
```

### **Verify System Status**
1. Check that both models are loaded:
   - `phishing_url_detector.pkl` (classification)
   - `threat_actor_profiler.pkl` (clustering)
2. Verify visualizations are generated:
   - `feature_importance.png`
   - `threat_clusters.png`
3. Confirm application is accessible at `http://localhost:8501`

## 📋 **Test Cases**

### **Test Case 1: Benign URL Analysis**

#### **Objective**
Validate that legitimate URLs are correctly classified as benign and no threat attribution is performed.

#### **Test Steps**
1. **Navigate to Application**
   - Open `http://localhost:8501`
   - Verify application loads without errors

2. **Configure Benign URL Features**
   - **URL Length**: Normal
   - **SSL Certificate Status**: Trusted
   - **Sub-domain Complexity**: None
   - **Prefix/Suffix**: Unchecked
   - **IP Address**: Unchecked
   - **Shortened URL**: Unchecked
   - **@ Symbol**: Unchecked
   - **Abnormal URL**: Unchecked
   - **Political Keywords**: Unchecked
   - **Technical Sophistication**: Low

3. **Execute Analysis**
   - Click "💥 Analyze & Initiate Response"
   - Wait for analysis to complete

4. **Verify Results**
   - **Tab 1 (Analysis Summary)**: Should show "BENIGN" with high confidence
   - **Tab 2 (Threat Attribution)**: Should show "No Threat Attribution Required"
   - **Tab 3 (Visual Insights)**: Should display risk contribution chart
   - **Tab 4 (Prescriptive Plan)**: Should show "No prescriptive plan generated"

#### **Expected Results**
- ✅ Classification: BENIGN
- ✅ Confidence Score: >80% for benign
- ✅ No threat actor profile assigned
- ✅ No prescriptive plan generated
- ✅ Risk contribution shows minimal risk factors

---

### **Test Case 2: Organized Cybercrime Attribution**

#### **Objective**
Validate that URLs with cybercrime characteristics are correctly classified as malicious and attributed to the Organized Cybercrime profile.

#### **Test Steps**
1. **Configure Cybercrime URL Features**
   - **URL Length**: Mixed (Normal)
   - **SSL Certificate Status**: Suspicious
   - **Sub-domain Complexity**: One
   - **Prefix/Suffix**: Checked
   - **IP Address**: Checked
   - **Shortened URL**: Checked
   - **@ Symbol**: Checked
   - **Abnormal URL**: Checked
   - **Political Keywords**: Unchecked
   - **Technical Sophistication**: Medium

2. **Execute Analysis**
   - Click "💥 Analyze & Initiate Response"
   - Wait for analysis to complete

3. **Verify Results**
   - **Tab 1**: Should show "MALICIOUS" with high confidence
   - **Tab 2**: Should show "🔴 Organized Cybercrime" profile
   - **Tab 3**: Should display risk contribution and cluster visualization
   - **Tab 4**: Should generate prescriptive response plan

#### **Expected Results**
- ✅ Classification: MALICIOUS
- ✅ Threat Actor: Organized Cybercrime (Cluster 0)
- ✅ Profile matches cybercrime characteristics
- ✅ GenAI prescription generated
- ✅ Risk factors align with cybercrime patterns

---

### **Test Case 3: State-Sponsored Attribution**

#### **Objective**
Validate that sophisticated URLs are correctly attributed to the State-Sponsored threat actor profile.

#### **Test Steps**
1. **Configure State-Sponsored URL Features**
   - **URL Length**: Long
   - **SSL Certificate Status**: None
   - **Sub-domain Complexity**: Many
   - **Prefix/Suffix**: Checked
   - **IP Address**: Unchecked
   - **Shortened URL**: Unchecked
   - **@ Symbol**: Unchecked
   - **Abnormal URL**: Checked
   - **Political Keywords**: Checked
   - **Technical Sophistication**: High

2. **Execute Analysis**
   - Click "💥 Analyze & Initiate Response"
   - Wait for analysis to complete

3. **Verify Results**
   - **Tab 1**: Should show "MALICIOUS" with high confidence
   - **Tab 2**: Should show "🔵 State-Sponsored" profile
   - **Tab 3**: Should display sophisticated risk patterns
   - **Tab 4**: Should generate targeted response plan

#### **Expected Results**
- ✅ Classification: MALICIOUS
- ✅ Threat Actor: State-Sponsored (Cluster 1)
- ✅ Profile shows high sophistication indicators
- ✅ Political targeting detected
- ✅ Advanced evasion techniques identified

---

### **Test Case 4: Hacktivist Attribution**

#### **Objective**
Validate that politically motivated URLs are correctly attributed to the Hacktivist threat actor profile.

#### **Test Steps**
1. **Configure Hacktivist URL Features**
   - **URL Length**: Normal
   - **SSL Certificate Status**: Suspicious
   - **Sub-domain Complexity**: One
   - **Prefix/Suffix**: Checked
   - **IP Address**: Unchecked
   - **Shortened URL**: Checked
   - **@ Symbol**: Checked
   - **Abnormal URL**: Checked
   - **Political Keywords**: Checked
   - **Technical Sophistication**: Medium

2. **Execute Analysis**
   - Click "💥 Analyze & Initiate Response"
   - Wait for analysis to complete

3. **Verify Results**
   - **Tab 1**: Should show "MALICIOUS" with high confidence
   - **Tab 2**: Should show "🟢 Hacktivist" profile
   - **Tab 3**: Should display mixed technical indicators
   - **Tab 4**: Should generate ideology-focused response plan

#### **Expected Results**
- ✅ Classification: MALICIOUS
- ✅ Threat Actor: Hacktivist (Cluster 2)
- ✅ Political motivation detected
- ✅ Mixed technical sophistication
- ✅ Ideological targeting identified

---

### **Test Case 5: GenAI Integration Testing**

#### **Objective**
Validate that different GenAI providers generate appropriate response plans.

#### **Test Steps**
1. **Test Each Provider**
   - Repeat a malicious URL test with each provider:
     - Gemini
     - OpenAI
     - Grok

2. **Verify Response Generation**
   - Check that each provider generates a response plan
   - Validate response plan structure and content
   - Ensure recommendations are appropriate for the threat profile

#### **Expected Results**
- ✅ All providers generate response plans
- ✅ Plans include recommended actions
- ✅ Communication drafts are generated
- ✅ Content is relevant to threat actor profile

---

### **Test Case 6: Model Training Validation**

#### **Objective**
Validate that both classification and clustering models train correctly and generate visualizations.

#### **Test Steps**
1. **Clean Environment**
   ```bash
   make clean
   ```

2. **Rebuild and Train**
   ```bash
   make up
   ```

3. **Monitor Training Process**
   ```bash
   make logs
   ```

4. **Verify Outputs**
   - Check `models/` directory for generated files
   - Validate model performance metrics
   - Confirm visualizations are created

#### **Expected Results**
- ✅ Both models train successfully
- ✅ Feature importance plot generated
- ✅ Cluster visualization created
- ✅ Models achieve reasonable accuracy
- ✅ Training completes without errors

---

### **Test Case 7: UI/UX Functionality**

#### **Objective**
Validate that all UI components function correctly across different scenarios.

#### **Test Steps**
1. **Test Sidebar Controls**
   - Verify all sliders and checkboxes work
   - Test form validation
   - Check responsive design

2. **Test Tab Navigation**
   - Verify all tabs load correctly
   - Test tab switching
   - Validate tab content updates

3. **Test Status Indicators**
   - Verify progress indicators work
   - Check error handling
   - Validate success states

#### **Expected Results**
- ✅ All UI controls responsive
- ✅ Tab navigation smooth
- ✅ Status updates clear
- ✅ Error messages helpful
- ✅ Responsive design works

---

### **Test Case 8: Performance Testing**

#### **Objective**
Validate system performance under normal load conditions.

#### **Test Steps**
1. **Measure Response Times**
   - Time URL analysis completion
   - Measure model loading time
   - Test concurrent user scenarios

2. **Resource Usage**
   - Monitor memory consumption
   - Check CPU usage during analysis
   - Validate Docker resource limits

#### **Expected Results**
- ✅ Analysis completes within 10 seconds
- ✅ Models load within 5 seconds
- ✅ Memory usage stays within limits
- ✅ CPU usage reasonable during analysis

## 🔍 **Validation Criteria**

### **Classification Model**
- **Accuracy**: >90% on test dataset
- **Precision**: >85% for malicious detection
- **Recall**: >80% for malicious detection
- **F1-Score**: >0.85

### **Clustering Model**
- **Silhouette Score**: >0.3 (reasonable clustering)
- **Cluster Separation**: Clear boundaries between profiles
- **Profile Accuracy**: >80% correct attribution

### **System Performance**
- **Response Time**: <10 seconds for complete analysis
- **Uptime**: >99% availability during testing
- **Error Rate**: <5% for user interactions

## 📊 **Test Results Documentation**

### **Test Execution Log**
```markdown
## Test Execution Summary

**Date**: [Date]
**Tester**: [Name]
**Environment**: [OS, Docker Version, etc.]

### Test Results
- [ ] Test Case 1: Benign URL Analysis
- [ ] Test Case 2: Organized Cybercrime Attribution
- [ ] Test Case 3: State-Sponsored Attribution
- [ ] Test Case 4: Hacktivist Attribution
- [ ] Test Case 5: GenAI Integration Testing
- [ ] Test Case 6: Model Training Validation
- [ ] Test Case 7: UI/UX Functionality
- [ ] Test Case 8: Performance Testing

### Issues Found
- [Issue description and severity]

### Recommendations
- [Action items for improvement]
```

## 🚨 **Troubleshooting Common Issues**

### **Model Loading Failures**
```bash
# Check model files exist
ls -la models/

# Verify file permissions
chmod 644 models/*.pkl

# Check container logs
make logs
```

### **Training Failures**
```bash
# Clean environment
make clean

# Check Docker resources
docker stats

# Verify Python dependencies
docker exec -it mini-soar pip list
```

### **UI Issues**
```bash
# Clear browser cache
# Check browser console for errors
# Verify Streamlit configuration
```

## 📝 **Reporting**

### **Test Report Template**
1. **Executive Summary**
   - Overall system status
   - Key findings
   - Risk assessment

2. **Detailed Results**
   - Test case outcomes
   - Performance metrics
   - Issue documentation

3. **Recommendations**
   - Immediate actions
   - Long-term improvements
   - Risk mitigation strategies

---

**Testing Complete** ✅

For questions or issues during testing, refer to the troubleshooting section or open a GitHub issue.
