# Rooms AI - AWS EC2 Deployment Guide

A LangGraph agent exposed as a FastAPI endpoint, managed with [uv](https://github.com/astral-sh/uv) and deployed on AWS EC2.

## 📋 Table of Contents

- [Local Development Setup](#-local-development-setup)
- [AWS EC2 Deployment](#-aws-ec2-deployment)

## 🚀 Local Development Setup

### Prerequisites

None! This guide will walk you through installing everything you need.

### Step 1: Install Python (if not already installed)

#### On Windows:

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **make sure to check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   ```

#### On macOS:

```bash
# Using Homebrew (recommended)
brew install python
```

#### On Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Install uv

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version

# Install the required Python version (3.11.4)
uv python install 3.11.4
```

### Step 3: Set up the Project

```bash
# Clone and setup
uv sync

# Verify correct Python version is being used
uv run python --version
# Should output: Python 3.11.4

# Run for development
uv run uvicorn main:app --reload --port 8000

# Run for production
uv run uvicorn main:app --port 8000
```

## ☁️ Deploying to AWS EC2

### Step 1: Create EC2 Instance

Log into your AWS account and create an EC2 instance (`t2.micro`), using the latest stable Ubuntu Linux AMI.

1. **Login to AWS Console**: Go to [AWS Console](https://console.aws.amazon.com/)
2. **Navigate to EC2**: Search for "EC2" in the services search bar
3. **Launch Instance**: Click "Launch Instance"
4. **Configure Instance**:
   - **Name**: `rooms-ai-server`
   - **AMI**: Select "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type" (latest stable)
   - **Instance Type**: `t2.micro`
   - **Key Pair**: Create new key pair and download the .pem file
   - **Network Settings**: Allow SSH and HTTP traffic from the internet
5. **Launch Instance**

### Step 2: Connect and Install Dependencies

SSH into the instance and run these commands to update the software repository and install our dependencies.

```bash
# Connect to your instance
ssh -i "your-keypair.pem" ubuntu@YOUR_EC2_PUBLIC_IP

# Update and install dependencies
sudo apt-get update
sudo apt install -y python3-pip nginx

# Install uv for Python package management
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Install Python 3.11.4 (required for your project)
uv python install 3.11.4
```

### Step 3: Clone and Setup Your Project

Clone your FastAPI server app (or create your `main.py` in Python).

```bash
# Clone your repository (replace with your actual repo URL)
git clone https://github.com/yourusername/rooms-ai.git

# Navigate to your project
cd rooms-ai

# Setup project with uv (will use Python 3.11.4 as specified in pyproject.toml)
uv sync

# Verify correct Python version
uv run python --version  # Should show Python 3.11.4
```

### Step 4: Configure Nginx

Add the FastAPI configuration to NGINX's folder. Create a file called `fastapi_nginx`.

```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):

```nginx
server {
    listen 80;
    server_name <YOUR_EC2_IP>;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Step 5: Start Services

Start NGINX:

```bash
sudo service nginx restart
```

Start FastAPI:

```bash
cd rooms-ai
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 6: Update Security Group

Update EC2 security-group settings for your instance to allow HTTP traffic to port 80.

1. Go to EC2 Dashboard → Security Groups
2. Select your instance's security group
3. Edit Inbound Rules
4. Add rule: HTTP (port 80) from 0.0.0.0/0

Now when you visit your public IP of the instance, you should be able to access your API.

### Phase 4: Configure Environment Variables

#### Step 1: Create Environment File

```bash
# Create .env file for production
nano .env
```

Add your environment variables:

```env
# Add your specific environment variables here
# Example:
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
ENVIRONMENT=production
```

**Access Your Application**: Once deployed, access your FastAPI application at:

- HTTP: `http://YOUR_EC2_PUBLIC_IP`
- HTTPS: `https://yourdomain.com` (if SSL configured)
- API Docs: `http://YOUR_EC2_PUBLIC_IP/docs`
