# Installation Guide - Cognitive SOAR System

This guide provides detailed instructions for setting up and deploying the Cognitive SOAR Threat Attribution System.

## 📋 **System Requirements**

### **Minimum Requirements**
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **CPU**: 4 cores (8 cores recommended)

### **Required Software**
- **Docker**: Version 20.10+ with Docker Compose
- **Git**: Version 2.20+
- **Make**: Version 4.0+ (optional but recommended)

## 🚀 **Installation Steps**

### **Step 1: Install Docker**

#### **Windows**
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the setup wizard
3. Ensure WSL 2 is enabled if prompted
4. Restart your computer
5. Verify installation: `docker --version`

#### **macOS**
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Drag Docker to Applications folder
3. Start Docker Desktop
4. Verify installation: `docker --version`

#### **Ubuntu/Debian**
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker compose version
```

### **Step 2: Install Make (Optional)**

#### **Windows**
```bash
# Using Chocolatey
choco install make

# Using WSL
sudo apt-get install make
```

#### **macOS**
```bash
# Using Homebrew
brew install make

# Or use the pre-installed version
make --version
```

#### **Ubuntu/Debian**
```bash
sudo apt-get install make
```

### **Step 3: Clone Repository**
```bash
git clone <repository-url>
cd cognitive-soar
```

### **Step 4: Configure API Keys**

#### **Create Streamlit Secrets Directory**
```bash
mkdir -p .streamlit
```

#### **Create Secrets File**
Create `.streamlit/secrets.toml` with your API keys:
```toml
# .streamlit/secrets.toml
# OpenAI API Key (required for OpenAI integration)
OPENAI_API_KEY = "sk-your-openai-api-key-here"

# Google Gemini API Key (required for Gemini integration)
GEMINI_API_KEY = "AIza-your-gemini-api-key-here"

# Grok API Key (required for Grok integration)
GROK_API_KEY = "gsk-your-grok-api-key-here"
```

**Note**: You only need to provide keys for the services you plan to use.

#### **API Key Setup Instructions**

##### **OpenAI API Key**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key and paste it in `secrets.toml`

##### **Google Gemini API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `secrets.toml`

##### **Grok API Key**
1. Visit [xAI Grok](https://console.x.ai/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key and paste it in `secrets.toml`

## 🏃 **First Run**

### **Step 1: Build and Start**
```bash
make up
```

**First Run Notes**:
- Initial build may take 5-10 minutes
- Docker will download base images and build the application
- Models will be trained automatically on first run
- Subsequent runs will be much faster

### **Step 2: Access Application**
Open your web browser and navigate to:
```
http://localhost:8501
```

### **Step 3: Verify Installation**
1. Check that the application loads without errors
2. Verify that both models are loaded (classification + clustering)
3. Test with a sample URL analysis

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using port 8501
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # macOS/Linux

# Stop the conflicting service or change port in docker-compose.yml
```

#### **Docker Permission Denied**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker service
sudo systemctl restart docker
```

#### **Model Training Fails**
```bash
# Check container logs
make logs

# Clean and rebuild
make clean
make up
```

#### **Memory Issues**
```bash
# Increase Docker memory limit in Docker Desktop settings
# Windows/macOS: Docker Desktop → Settings → Resources → Memory
# Linux: Edit /etc/docker/daemon.json
```

### **Log Analysis**
```bash
# View real-time logs
make logs

# View specific service logs
docker compose logs mini-soar-app

# Check container status
docker compose ps
```

## 📊 **Performance Optimization**

### **Docker Settings**
- **Memory**: Allocate at least 8GB to Docker
- **CPU**: Allocate at least 4 cores
- **Swap**: Enable swap for better memory management

### **System Optimization**
- **Close unnecessary applications** during training
- **Ensure adequate free disk space** (10GB+)
- **Use SSD storage** for better I/O performance

## 🔒 **Security Considerations**

### **API Key Security**
- **Never commit API keys** to version control
- **Use environment variables** in production
- **Rotate keys regularly** for production use
- **Limit API key permissions** to minimum required

### **Network Security**
- **Firewall configuration**: Only expose necessary ports
- **VPN usage**: Consider VPN for remote access
- **HTTPS**: Use reverse proxy with SSL in production

## 🚀 **Production Deployment**

### **Environment Variables**
```bash
# Production environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export PYTHONPATH=/app
```

### **Reverse Proxy Setup**
```nginx
# Nginx configuration example
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **SSL/TLS Configuration**
```bash
# Using Let's Encrypt
sudo certbot --nginx -d your-domain.com

# Or manual SSL certificate setup
# Place certificates in /etc/ssl/certs/
```

## 📚 **Additional Resources**

- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyCaret Documentation](https://pycaret.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🆘 **Getting Help**

### **Support Channels**
1. **GitHub Issues**: Report bugs and feature requests
2. **Documentation**: Check README.md and TESTING.md
3. **Community**: Join our community discussions
4. **Email**: Contact the development team

### **Debug Information**
When reporting issues, include:
- Operating system and version
- Docker version
- Application logs
- Error messages
- Steps to reproduce

---

**Need Help?** Check the troubleshooting section above or open a GitHub issue for support.
