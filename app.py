# app.py
import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
from pycaret.clustering import load_model as load_clustering_model, predict_model as predict_clustering
from genai_prescriptions import generate_prescription
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Cognitive SOAR - Threat Attribution System",
    page_icon="🛡️",
    layout="wide"
)

# --- Threat Actor Profile Descriptions ---
THREAT_ACTOR_PROFILES = {
    0: {
        "name": "Organized Cybercrime",
        "description": "High-volume, financially motivated threat actors using automated tools and infrastructure.",
        "characteristics": [
            "Frequent use of IP addresses and URL shortening services",
            "High volume of abnormal URL structures",
            "Moderate sophistication with focus on quantity over quality",
            "Targets financial gain through phishing campaigns"
        ],
        "motivations": "Financial profit through credential theft, credit card fraud, and ransomware deployment",
        "typical_targets": "Financial institutions, e-commerce sites, healthcare organizations",
        "color": "red"
    },
    1: {
        "name": "State-Sponsored",
        "description": "Nation-state actors with high sophistication and strategic objectives.",
        "characteristics": [
            "Advanced evasion techniques and complex URL structures",
            "High use of prefix/suffix manipulation and subdomain complexity",
            "Poor SSL certificate usage for stealth",
            "Targeted political and strategic intelligence gathering"
        ],
        "motivations": "Intelligence collection, political espionage, and strategic advantage",
        "typical_targets": "Government agencies, defense contractors, critical infrastructure",
        "color": "blue"
    },
    2: {
        "name": "Hacktivist",
        "description": "Ideologically motivated actors with mixed technical capabilities.",
        "characteristics": [
            "High political keyword usage in campaigns",
            "Mixed technical sophistication levels",
            "Balanced approach to URL manipulation techniques",
            "Focus on ideological messaging and disruption"
        ],
        "motivations": "Political activism, social justice, and ideological statements",
        "typical_targets": "Government websites, corporations, political organizations",
        "color": "green"
    }
}

# --- Load Models and Assets ---
@st.cache_resource
def load_assets():
    """Load both classification and clustering models along with visualizations."""
    model_path = 'models/phishing_url_detector'
    clustering_model_path = 'models/threat_actor_profiler'
    plot_path = 'models/feature_importance.png'
    cluster_plot_path = 'models/threat_clusters.png'
    
    classification_model = None
    clustering_model = None
    feature_plot = None
    cluster_plot = None
    
    if os.path.exists(model_path + '.pkl'):
        classification_model = load_model(model_path)
    if os.path.exists(clustering_model_path + '.pkl'):
        clustering_model = load_model(clustering_model_path)
    if os.path.exists(plot_path):
        feature_plot = plot_path
    if os.path.exists(cluster_plot_path):
        cluster_plot = cluster_plot_path
        
    return classification_model, clustering_model, feature_plot, cluster_plot


classification_model, clustering_model, feature_plot, cluster_plot = load_assets()

if not classification_model or not clustering_model:
    st.error(
        "Models not found. Please wait for the initial training to complete, or check the container logs with `make logs` if the error persists.")
    st.stop()

# --- Sidebar for Inputs ---
with st.sidebar:
    st.title("🔬 URL Feature Input")
    st.write("Describe the characteristics of a suspicious URL below.")

    # Using a dictionary to hold form values
    form_values = {
        'url_length': st.select_slider("URL Length", options=['Short', 'Normal', 'Long'], value='Long'),
        'ssl_state': st.select_slider("SSL Certificate Status", options=['Trusted', 'Suspicious', 'None'],
                                      value='Suspicious'),
        'sub_domain': st.select_slider("Sub-domain Complexity", options=['None', 'One', 'Many'], value='One'),
        'prefix_suffix': st.checkbox("URL has a Prefix/Suffix (e.g.,'-')", value=True),
        'has_ip': st.checkbox("URL uses an IP Address", value=False),
        'short_service': st.checkbox("Is it a shortened URL", value=False),
        'at_symbol': st.checkbox("URL contains '@' symbol", value=False),
        'abnormal_url': st.checkbox("Is it an abnormal URL", value=True),
        'political_keyword': st.checkbox("Contains political keywords", value=False),
        'sophistication': st.select_slider("Technical Sophistication", options=['Low', 'Medium', 'High'], value='Medium'),
    }

    st.divider()
    genai_provider = st.selectbox("Select GenAI Provider", ["Gemini", "OpenAI", "Grok"])
    submitted = st.button("💥 Analyze & Initiate Response", use_container_width=True, type="primary")

# --- Main Page ---
st.title("🛡️ Cognitive SOAR - Threat Attribution System")
st.markdown("**From Prediction to Attribution: Intelligent Threat Analysis**")

if not submitted:
    st.info("Please provide the URL features in the sidebar and click 'Analyze' to begin.")
    
    # Display model information
    col1, col2 = st.columns(2)
    with col1:
        if feature_plot:
            st.subheader("Classification Model Features")
            st.image(feature_plot, caption="Feature importance from the trained classification model.")
    
    with col2:
        if cluster_plot:
            st.subheader("Threat Actor Clustering")
            st.image(cluster_plot, caption="Visualization of threat actor clusters discovered by the system.")

else:
    # --- Data Preparation and Risk Scoring ---
    input_dict = {
        'having_IP_Address': 1 if form_values['has_ip'] else -1,
        'URL_Length': -1 if form_values['url_length'] == 'Short' else (
            0 if form_values['url_length'] == 'Normal' else 1),
        'Shortining_Service': 1 if form_values['short_service'] else -1,
        'having_At_Symbol': 1 if form_values['at_symbol'] else -1,
        'double_slash_redirecting': -1,
        'Prefix_Suffix': 1 if form_values['prefix_suffix'] else -1,
        'having_Sub_Domain': -1 if form_values['sub_domain'] == 'None' else (
            0 if form_values['sub_domain'] == 'One' else 1),
        'SSLfinal_State': -1 if form_values['ssl_state'] == 'None' else (
            0 if form_values['ssl_state'] == 'Suspicious' else 1),
        'Abnormal_URL': 1 if form_values['abnormal_url'] else -1,
        'URL_of_Anchor': 0, 'Links_in_tags': 0, 'SFH': 0,
        'has_political_keyword': 1 if form_values['political_keyword'] else -1,
        'sophistication_level': -1 if form_values['sophistication'] == 'Low' else (
            0 if form_values['sophistication'] == 'Medium' else 1),
    }
    input_data = pd.DataFrame([input_dict])

    # Simple risk contribution for visualization
    risk_scores = {
        "Bad SSL": 25 if input_dict['SSLfinal_State'] < 1 else 0,
        "Abnormal URL": 20 if input_dict['Abnormal_URL'] == 1 else 0,
        "Prefix/Suffix": 15 if input_dict['Prefix_Suffix'] == 1 else 0,
        "Shortened URL": 15 if input_dict['Shortining_Service'] == 1 else 0,
        "Complex Sub-domain": 10 if input_dict['having_Sub_Domain'] == 1 else 0,
        "Long URL": 10 if input_dict['URL_Length'] == 1 else 0,
        "Uses IP Address": 5 if input_dict['having_IP_Address'] == 1 else 0,
        "Political Keywords": 10 if input_dict['has_political_keyword'] == 1 else 0,
        "High Sophistication": 15 if input_dict['sophistication_level'] == 1 else 0,
    }
    risk_df = pd.DataFrame(list(risk_scores.items()), columns=['Feature', 'Risk Contribution']).sort_values(
        'Risk Contribution', ascending=False)

    # --- Analysis Workflow ---
    with st.status("Executing Cognitive SOAR playbook...", expanded=True) as status:
        st.write("▶️ **Step 1: Predictive Analysis** - Running features through classification model.")
        time.sleep(1)
        prediction = predict_model(classification_model, data=input_data)
        is_malicious = prediction['prediction_label'].iloc[0] == 1

        verdict = "MALICIOUS" if is_malicious else "BENIGN"
        st.write(f"▶️ **Step 2: Verdict Interpretation** - Model predicts **{verdict}**.")
        time.sleep(1)

        if is_malicious:
            st.write("▶️ **Step 3: Threat Attribution** - Analyzing threat actor profile.")
            time.sleep(1)
            
            # Run clustering model for threat attribution
            cluster_prediction = predict_clustering(clustering_model, data=input_data)
            cluster_id = cluster_prediction['Cluster'].iloc[0]
            
            threat_profile = THREAT_ACTOR_PROFILES.get(cluster_id, {
                "name": "Unknown Threat Actor",
                "description": "Unable to determine threat actor profile.",
                "characteristics": [],
                "motivations": "Unknown",
                "typical_targets": "Unknown",
                "color": "gray"
            })
            
            st.write(f"▶️ **Step 4: Prescriptive Analytics** - Engaging **{genai_provider}** for action plan.")
            try:
                prescription = generate_prescription(genai_provider, {k: v for k, v in input_dict.items()})
                status.update(label="✅ Cognitive SOAR Playbook Executed Successfully!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Failed to generate prescription: {e}")
                prescription = None
                status.update(label="🚨 Error during GenAI prescription!", state="error")
        else:
            threat_profile = None
            cluster_id = None
            prescription = None
            status.update(label="✅ Analysis Complete. No threat found.", state="complete", expanded=False)

    # --- Tabs for Organized Output ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 **Analysis Summary**", 
        "🎯 **Threat Attribution**", 
        "📈 **Visual Insights**", 
        "📜 **Prescriptive Plan**"
    ])

    with tab1:
        st.subheader("Verdict and Key Findings")
        if is_malicious:
            st.error("**Prediction: Malicious Phishing URL**", icon="🚨")
        else:
            st.success("**Prediction: Benign URL**", icon="✅")

        st.metric("Malicious Confidence Score",
                  f"{prediction['prediction_score'].iloc[0]:.2%}" if is_malicious else f"{1 - prediction['prediction_score'].iloc[0]:.2%}")
        st.caption("This score represents the model's confidence in its prediction.")

    with tab2:
        st.subheader("Threat Actor Attribution")
        if is_malicious and threat_profile:
            # Display threat actor profile
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"### 🎯 **{threat_profile['name']}**")
                st.markdown(f"**Cluster ID:** {cluster_id}")
                
                # Color-coded threat level
                threat_colors = {"red": "🔴", "blue": "🔵", "green": "🟢"}
                st.markdown(f"**Threat Level:** {threat_colors.get(threat_profile['color'], '⚪')} {threat_profile['name']}")
            
            with col2:
                st.markdown("#### **Profile Description**")
                st.info(threat_profile['description'])
                
                st.markdown("#### **Key Characteristics**")
                for char in threat_profile['characteristics']:
                    st.markdown(f"• {char}")
            
            # Additional details
            st.markdown("#### **Motivations & Targets**")
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("**Primary Motivation:**")
                st.write(threat_profile['motivations'])
            with col4:
                st.markdown("**Typical Targets:**")
                st.write(threat_profile['typical_targets'])
                
        elif not is_malicious:
            st.success("✅ **No Threat Attribution Required**")
            st.info("The URL was classified as benign, so no threat actor analysis was performed.")
        else:
            st.warning("⚠️ **Threat Attribution Unavailable**")
            st.error("Unable to determine threat actor profile for this malicious URL.")

    with tab3:
        st.subheader("Visual Analysis")
        st.write("#### Risk Contribution by Feature")
        st.bar_chart(risk_df.set_index('Feature'))
        st.caption("A simplified view of which input features contributed most to a higher risk score.")

        if feature_plot:
            st.write("#### Classification Model Feature Importance (Global)")
            st.image(feature_plot,
                     caption="This plot shows which features the classification model found most important *overall* during its training.")
        
        if cluster_plot:
            st.write("#### Threat Actor Clustering Visualization")
            st.image(cluster_plot,
                     caption="This visualization shows how the system groups different threat actor profiles based on URL characteristics.")

    with tab4:
        st.subheader("Actionable Response Plan")
        if prescription:
            st.success("A prescriptive response plan has been generated by the AI.", icon="🤖")
            st.json(prescription, expanded=False)  # Show the raw JSON for transparency

            st.write("#### Recommended Actions (for Security Analyst)")
            for i, action in enumerate(prescription.get("recommended_actions", []), 1):
                st.markdown(f"**{i}.** {action}")

            st.write("#### Communication Draft (for End-User/Reporter)")
            st.text_area("Draft", prescription.get("communication_draft", ""), height=150)
        else:
            st.info("No prescriptive plan was generated because the URL was classified as benign.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "**Cognitive SOAR System** - Advanced threat detection with intelligent attribution capabilities. "
    "Built with PyCaret, Streamlit, and Docker."
)

