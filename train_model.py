# train_model.py
import pandas as pd
import numpy as np
from pycaret.classification import *
from pycaret.clustering import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def generate_synthetic_data(num_samples=1000):
    """Generates a synthetic dataset of phishing and benign URL features with threat actor profiles."""
    print("Generating synthetic dataset with threat actor profiles...")

    features = [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'URL_of_Anchor', 'Links_in_tags',
        'SFH', 'Abnormal_URL', 'has_political_keyword', 'sophistication_level'
    ]

    num_phishing = num_samples // 2
    num_benign = num_samples - num_phishing

    # Threat Actor Profile 1: State-Sponsored (High sophistication, deceptive techniques)
    state_sponsored = num_phishing // 3
    state_sponsored_data = {
        'having_IP_Address': np.random.choice([1, -1], state_sponsored, p=[0.1, 0.9]),  # Low IP usage
        'URL_Length': np.random.choice([1, 0, -1], state_sponsored, p=[0.7, 0.2, 0.1]),  # Long URLs
        'Shortining_Service': np.random.choice([1, -1], state_sponsored, p=[0.2, 0.8]),  # Avoid shortening
        'having_At_Symbol': np.random.choice([1, -1], state_sponsored, p=[0.3, 0.7]),
        'double_slash_redirecting': np.random.choice([1, -1], state_sponsored, p=[0.4, 0.6]),
        'Prefix_Suffix': np.random.choice([1, -1], state_sponsored, p=[0.8, 0.2]),  # High prefix/suffix
        'having_Sub_Domain': np.random.choice([1, 0, -1], state_sponsored, p=[0.7, 0.2, 0.1]),  # Complex subdomains
        'SSLfinal_State': np.random.choice([-1, 0, 1], state_sponsored, p=[0.7, 0.2, 0.1]),  # Poor SSL
        'URL_of_Anchor': np.random.choice([-1, 0, 1], state_sponsored, p=[0.6, 0.3, 0.1]),
        'Links_in_tags': np.random.choice([-1, 0, 1], state_sponsored, p=[0.5, 0.3, 0.2]),
        'SFH': np.random.choice([-1, 0, 1], state_sponsored, p=[0.7, 0.2, 0.1]),
        'Abnormal_URL': np.random.choice([1, -1], state_sponsored, p=[0.6, 0.4]),
        'has_political_keyword': np.random.choice([1, -1], state_sponsored, p=[0.3, 0.7]),  # Some political targeting
        'sophistication_level': np.random.choice([1, 0, -1], state_sponsored, p=[0.8, 0.15, 0.05])  # High sophistication
    }

    # Threat Actor Profile 2: Organized Cybercrime (High-volume, noisy attacks)
    cybercrime = num_phishing // 3
    cybercrime_data = {
        'having_IP_Address': np.random.choice([1, -1], cybercrime, p=[0.6, 0.4]),  # High IP usage
        'URL_Length': np.random.choice([1, 0, -1], cybercrime, p=[0.2, 0.5, 0.3]),  # Mixed lengths
        'Shortining_Service': np.random.choice([1, -1], cybercrime, p=[0.8, 0.2]),  # High shortening usage
        'having_At_Symbol': np.random.choice([1, -1], cybercrime, p=[0.5, 0.5]),
        'double_slash_redirecting': np.random.choice([1, -1], cybercrime, p=[0.6, 0.4]),
        'Prefix_Suffix': np.random.choice([1, -1], cybercrime, p=[0.4, 0.6]),  # Moderate prefix/suffix
        'having_Sub_Domain': np.random.choice([1, 0, -1], cybercrime, p=[0.3, 0.4, 0.3]),
        'SSLfinal_State': np.random.choice([-1, 0, 1], cybercrime, p=[0.5, 0.3, 0.2]),
        'URL_of_Anchor': np.random.choice([-1, 0, 1], cybercrime, p=[0.4, 0.4, 0.2]),
        'Links_in_tags': np.random.choice([-1, 0, 1], cybercrime, p=[0.5, 0.3, 0.2]),
        'SFH': np.random.choice([-1, 0, 1], cybercrime, p=[0.6, 0.2, 0.2]),
        'Abnormal_URL': np.random.choice([1, -1], cybercrime, p=[0.7, 0.3]),  # High abnormal URLs
        'has_political_keyword': np.random.choice([1, -1], cybercrime, p=[0.1, 0.9]),  # Low political targeting
        'sophistication_level': np.random.choice([1, 0, -1], cybercrime, p=[0.2, 0.5, 0.3])  # Medium sophistication
    }

    # Threat Actor Profile 3: Hacktivist (Mix of tactics, political motivation)
    hacktivist = num_phishing - state_sponsored - cybercrime
    hacktivist_data = {
        'having_IP_Address': np.random.choice([1, -1], hacktivist, p=[0.4, 0.6]),
        'URL_Length': np.random.choice([1, 0, -1], hacktivist, p=[0.3, 0.4, 0.3]),
        'Shortining_Service': np.random.choice([1, -1], hacktivist, p=[0.5, 0.5]),
        'having_At_Symbol': np.random.choice([1, -1], hacktivist, p=[0.4, 0.6]),
        'double_slash_redirecting': np.random.choice([1, -1], hacktivist, p=[0.4, 0.6]),
        'Prefix_Suffix': np.random.choice([1, -1], hacktivist, p=[0.5, 0.5]),
        'having_Sub_Domain': np.random.choice([1, 0, -1], hacktivist, p=[0.4, 0.4, 0.2]),
        'SSLfinal_State': np.random.choice([-1, 0, 1], hacktivist, p=[0.4, 0.3, 0.3]),
        'URL_of_Anchor': np.random.choice([-1, 0, 1], hacktivist, p=[0.4, 0.3, 0.3]),
        'Links_in_tags': np.random.choice([-1, 0, 1], hacktivist, p=[0.4, 0.3, 0.3]),
        'SFH': np.random.choice([-1, 0, 1], hacktivist, p=[0.4, 0.3, 0.3]),
        'Abnormal_URL': np.random.choice([1, -1], hacktivist, p=[0.5, 0.5]),
        'has_political_keyword': np.random.choice([1, -1], hacktivist, p=[0.7, 0.3]),  # High political targeting
        'sophistication_level': np.random.choice([1, 0, -1], hacktivist, p=[0.3, 0.5, 0.2])  # Medium sophistication
    }

    # Benign data (same as before)
    benign_data = {
        'having_IP_Address': np.random.choice([1, -1], num_benign, p=[0.05, 0.95]),
        'URL_Length': np.random.choice([1, 0, -1], num_benign, p=[0.1, 0.6, 0.3]),
        'Shortining_Service': np.random.choice([1, -1], num_benign, p=[0.1, 0.9]),
        'having_At_Symbol': np.random.choice([1, -1], num_benign, p=[0.05, 0.95]),
        'double_slash_redirecting': np.random.choice([1, -1], num_benign, p=[0.05, 0.95]),
        'Prefix_Suffix': np.random.choice([1, -1], num_benign, p=[0.1, 0.9]),
        'having_Sub_Domain': np.random.choice([1, 0, -1], num_benign, p=[0.1, 0.4, 0.5]),
        'SSLfinal_State': np.random.choice([-1, 0, 1], num_benign, p=[0.05, 0.15, 0.8]),
        'URL_of_Anchor': np.random.choice([-1, 0, 1], num_benign, p=[0.1, 0.2, 0.7]),
        'Links_in_tags': np.random.choice([-1, 0, 1], num_benign, p=[0.1, 0.2, 0.7]),
        'SFH': np.random.choice([-1, 0, 1], num_benign, p=[0.1, 0.1, 0.8]),
        'Abnormal_URL': np.random.choice([1, -1], num_benign, p=[0.1, 0.9]),
        'has_political_keyword': np.random.choice([1, -1], num_benign, p=[0.05, 0.95]),
        'sophistication_level': np.random.choice([1, 0, -1], num_benign, p=[0.05, 0.1, 0.85])
    }

    # Create DataFrames with threat actor labels
    df_state_sponsored = pd.DataFrame(state_sponsored_data)
    df_cybercrime = pd.DataFrame(cybercrime_data)
    df_hacktivist = pd.DataFrame(hacktivist_data)
    df_benign = pd.DataFrame(benign_data)

    # Add labels
    df_state_sponsored['label'] = 1
    df_state_sponsored['threat_actor'] = 0  # Cluster 0
    df_cybercrime['label'] = 1
    df_cybercrime['threat_actor'] = 1      # Cluster 1
    df_hacktivist['label'] = 1
    df_hacktivist['threat_actor'] = 2      # Cluster 2
    df_benign['label'] = 0
    df_benign['threat_actor'] = -1         # No threat actor for benign

    # Combine all data
    final_df = pd.concat([df_state_sponsored, df_cybercrime, df_hacktivist, df_benign], ignore_index=True)
    return final_df.sample(frac=1).reset_index(drop=True)


def train_classification_model(data):
    """Train the phishing classification model."""
    print("Training classification model...")
    
    # Setup PyCaret for classification
    s = setup(data, target='label', session_id=42, verbose=False)
    
    print("Comparing classification models...")
    best_model = compare_models(n_select=1, include=['rf', 'et', 'lightgbm'])
    
    print("Finalizing classification model...")
    final_model = finalize_model(best_model)
    
    return final_model


def train_clustering_model(data):
    """Train the threat actor clustering model."""
    print("Training clustering model...")
    
    # Remove label and threat_actor columns for clustering
    clustering_data = data.drop(['label', 'threat_actor'], axis=1)
    
    # Setup PyCaret for clustering
    s = setup(clustering_data, session_id=42, verbose=False)
    
    print("Training K-Means clustering model...")
    kmeans_model = create_model('kmeans', num_clusters=3)
    
    print("Finalizing clustering model...")
    final_clustering_model = finalize_model(kmeans_model)
    
    return final_clustering_model


def create_cluster_visualization(data, clustering_model, save_path):
    """Create and save cluster visualization."""
    print("Creating cluster visualization...")
    
    # Get cluster predictions
    clustering_data = data.drop(['label', 'threat_actor'], axis=1)
    cluster_predictions = predict_model(clustering_model, data=clustering_data)
    
    # Add cluster predictions to data
    data_with_clusters = data.copy()
    data_with_clusters['predicted_cluster'] = cluster_predictions['Cluster']
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    
    # Use PCA for dimensionality reduction for visualization
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    features_2d = pca.fit_transform(clustering_data)
    
    # Create scatter plot
    scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], 
                         c=data_with_clusters['predicted_cluster'], 
                         cmap='viridis', alpha=0.7)
    
    plt.title('Threat Actor Clusters Visualization', fontsize=16)
    plt.xlabel('Principal Component 1', fontsize=12)
    plt.ylabel('Principal Component 2', fontsize=12)
    plt.colorbar(scatter, label='Cluster ID')
    
    # Add cluster labels
    cluster_labels = ['Organized Cybercrime', 'State-Sponsored', 'Hacktivist']
    for i, label in enumerate(cluster_labels):
        cluster_points = features_2d[data_with_clusters['predicted_cluster'] == i]
        if len(cluster_points) > 0:
            centroid = cluster_points.mean(axis=0)
            plt.annotate(label, centroid, fontsize=10, ha='center', 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Cluster visualization saved to {save_path}")


def train():
    """Main training function for both classification and clustering models."""
    model_path = 'models/phishing_url_detector'
    clustering_model_path = 'models/threat_actor_profiler'
    plot_path = 'models/feature_importance.png'
    cluster_plot_path = 'models/threat_clusters.png'

    if os.path.exists(model_path + '.pkl') and os.path.exists(clustering_model_path + '.pkl'):
        print("Models already exist. Skipping training.")
        return

    # Generate synthetic data
    data = generate_synthetic_data()
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/phishing_synthetic.csv', index=False)

    # Create models directory
    os.makedirs('models', exist_ok=True)

    # Train classification model
    classification_model = train_classification_model(data)
    
    # Train clustering model
    clustering_model = train_clustering_model(data)

    # Save models
    print("Saving classification model...")
    save_model(classification_model, model_path)
    
    print("Saving clustering model...")
    save_model(clustering_model, clustering_model_path)

    # Create and save visualizations
    print("Creating feature importance plot...")
    plot_model(classification_model, plot='feature', save=True)
    os.rename('Feature Importance.png', plot_path)
    
    print("Creating cluster visualization...")
    create_cluster_visualization(data, clustering_model, cluster_plot_path)

    print("All models and visualizations saved successfully!")


if __name__ == "__main__":
    train()