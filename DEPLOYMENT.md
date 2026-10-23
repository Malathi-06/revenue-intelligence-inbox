# Revenue Intelligence Inbox - Deployment Guide

This guide covers multiple deployment options for the Revenue Intelligence Inbox application.

⚠️ **Important:** All sample data is SYNTHETIC. Replace with production data before deployment.

---

## Table of Contents

1. [Streamlit Cloud (Easiest)](#streamlit-cloud)
2. [Heroku](#heroku)
3. [AWS (EC2 + RDS)](#aws-deployment)
4. [Docker](#docker-deployment)
5. [Azure](#azure-deployment)
6. [Google Cloud Platform](#gcp-deployment)

---

## Prerequisites for All Deployments

### 1. Environment Variables
Create a `.env` file with:
```env
# Database (use PostgreSQL for production)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Optional: Application settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 2. Database Migration
Replace SQLite with PostgreSQL for production:
```python
# Update src/utils/config.py
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://...')
```

### 3. Dependencies
Ensure `requirements.txt` is complete (already provided).

---

## Streamlit Cloud

**Best for:** Quick demos, prototypes, small teams  
**Cost:** Free tier available  
**Time:** ~5 minutes

### Steps

1. **Push to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Revenue Intelligence Inbox"
   git branch -M main
   git remote add origin https://github.com/yourusername/revenue-intelligence-inbox.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `revenue-intelligence-inbox`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets:**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
   ```toml
   [database]
   url = "postgresql://user:password@host:5432/dbname"
   ```

4. **Update Database Connection:**
   - Update `src/utils/config.py` to read from Streamlit secrets
   - Or use environment variables

**Your app will be live at:** `https://yourapp.streamlit.app`

---

## Heroku

**Best for:** Small to medium production apps  
**Cost:** Starts at $7/month  
**Time:** ~15 minutes

### Steps

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App:**
   ```bash
   heroku login
   heroku create revenue-intelligence-inbox
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Create Procfile:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

5. **Create setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

6. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   heroku open
   ```

7. **Initialize Database:**
   ```bash
   heroku run python init_db.py
   ```

**Your app will be live at:** `https://revenue-intelligence-inbox.herokuapp.com`

---

## Docker Deployment

**Best for:** Consistent environments, any cloud provider  
**Time:** ~20 minutes

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data /app/exports

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/revenue_intelligence
    depends_on:
      - db
    volumes:
      - ./data:/app/data
      - ./exports:/app/exports

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=revenue_intelligence
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3. Build and Run

```bash
# Build image
docker build -t revenue-intelligence-inbox .

# Run with docker-compose
docker-compose up -d

# Initialize database
docker-compose exec app python init_db.py

# View logs
docker-compose logs -f app

# Access application
# http://localhost:8501
```

### 4. Deploy to Any Cloud

```bash
# Tag image
docker tag revenue-intelligence-inbox your-registry/revenue-intelligence-inbox:latest

# Push to registry
docker push your-registry/revenue-intelligence-inbox:latest

# Deploy on cloud platform (AWS ECS, Azure Container Instances, GCP Cloud Run, etc.)
```

---

## AWS Deployment

**Best for:** Enterprise production, scalability  
**Cost:** Variable (EC2 + RDS)  
**Time:** ~45 minutes

### Option A: EC2 + RDS (Traditional)

#### 1. Create RDS PostgreSQL Instance
```bash
aws rds create-db-instance \
  --db-instance-identifier revenue-intelligence-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourSecurePassword \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx
```

#### 2. Launch EC2 Instance
```bash
# Launch Ubuntu 22.04 instance (t2.micro or larger)
# SSH into instance
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com
```

#### 3. Install Dependencies on EC2
```bash
sudo apt update
sudo apt install -y python3-pip git
git clone https://github.com/yourusername/revenue-intelligence-inbox.git
cd revenue-intelligence-inbox
pip3 install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://admin:YourSecurePassword@revenue-intelligence-db.xxxxx.rds.amazonaws.com:5432/postgres
EOF
```

#### 5. Run with systemd
```bash
# Create service file
sudo cat > /etc/systemd/system/revenue-intelligence.service <<EOF
[Unit]
Description=Revenue Intelligence Inbox
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/revenue-intelligence-inbox
ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable revenue-intelligence
sudo systemctl start revenue-intelligence
```

#### 6. Configure Security Group
- Allow inbound on port 8501 (or 80/443 with reverse proxy)

### Option B: AWS Elastic Beanstalk (Easier)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 revenue-intelligence-inbox

# Create environment with RDS
eb create revenue-intelligence-env --database.engine postgres

# Deploy
eb deploy

# Open application
eb open
```

---

## Azure Deployment

**Best for:** Microsoft ecosystem  
**Time:** ~30 minutes

### 1. Create Azure Resources

```bash
# Install Azure CLI
# Download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name revenue-intelligence-rg --location eastus

# Create PostgreSQL
az postgres flexible-server create \
  --resource-group revenue-intelligence-rg \
  --name revenue-intelligence-db \
  --location eastus \
  --admin-user adminuser \
  --admin-password YourSecurePassword \
  --sku-name Standard_B1ms

# Create App Service
az webapp up \
  --resource-group revenue-intelligence-rg \
  --name revenue-intelligence-inbox \
  --runtime "PYTHON:3.11" \
  --sku B1
```

### 2. Configure Application Settings

```bash
# Set environment variables
az webapp config appsettings set \
  --resource-group revenue-intelligence-rg \
  --name revenue-intelligence-inbox \
  --settings DATABASE_URL="postgresql://adminuser:YourSecurePassword@revenue-intelligence-db.postgres.database.azure.com:5432/postgres"
```

### 3. Deploy

```bash
# Deploy from local git
git remote add azure https://revenue-intelligence-inbox.scm.azurewebsites.net/revenue-intelligence-inbox.git
git push azure main
```

**Your app will be live at:** `https://revenue-intelligence-inbox.azurewebsites.net`

---

## GCP Deployment

**Best for:** Google Cloud ecosystem  
**Time:** ~30 minutes

### Option A: Cloud Run (Serverless)

```bash
# Install gcloud CLI
# Download from https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project your-project-id

# Build and deploy
gcloud run deploy revenue-intelligence-inbox \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...
```

### Option B: App Engine

```bash
# Create app.yaml
cat > app.yaml <<EOF
runtime: python311
entrypoint: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0

env_variables:
  DATABASE_URL: "postgresql://..."
EOF

# Deploy
gcloud app deploy
```

### Create Cloud SQL PostgreSQL

```bash
gcloud sql instances create revenue-intelligence-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

---

## Post-Deployment Checklist

### Security
- [ ] Update default passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up authentication (if needed)
- [ ] Review security groups/network policies

### Database
- [ ] Replace SQLite with PostgreSQL
- [ ] Run database migrations: `python init_db.py`
- [ ] Replace synthetic data with production data
- [ ] Set up automated backups
- [ ] Configure connection pooling

### Monitoring
- [ ] Set up application logging
- [ ] Configure error tracking (Sentry, Rollbar)
- [ ] Enable performance monitoring
- [ ] Set up uptime monitoring
- [ ] Configure alerts

### Application
- [ ] Test all features in production
- [ ] Verify routing engine works correctly
- [ ] Test import/export functionality
- [ ] Validate analytics calculations
- [ ] Check manual edit protection

### Documentation
- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Set up team access

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `STREAMLIT_SERVER_PORT` | Application port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Bind address | `0.0.0.0` |
| `SECRET_KEY` | Session secret (if auth added) | Random string |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://...'); print(engine.connect())"
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8501  # Unix/Mac
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 <PID>  # Unix/Mac
taskkill /PID <PID> /F  # Windows
```

### Memory Issues
- Increase instance size
- Enable connection pooling
- Optimize database queries

### Slow Performance
- Add database indexes
- Enable caching in Streamlit
- Use CDN for static assets
- Upgrade instance tier

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (ALB, Azure Load Balancer, GCP Load Balancer)
- Run multiple app instances
- Share PostgreSQL database
- Use Redis for session management

### Vertical Scaling
- Upgrade instance size
- Increase database resources
- Add read replicas

### Caching
```python
# Add to app.py
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_dashboard_data():
    # Expensive operations
    pass
```

---

## Cost Estimates

| Platform | Free Tier | Paid (Small) | Paid (Medium) |
|----------|-----------|--------------|---------------|
| **Streamlit Cloud** | Yes (1 app) | $0 | $0 |
| **Heroku** | No | $7-25/mo | $25-50/mo |
| **AWS** | 12 months | $20-40/mo | $50-100/mo |
| **Azure** | 12 months | $15-35/mo | $40-80/mo |
| **GCP** | $300 credit | $15-30/mo | $40-75/mo |

*Estimates include compute + database. Actual costs vary by usage.*

---

## Recommended Deployment Path

### For Demo/POC
1. **Streamlit Cloud** - Fastest, free, perfect for demos

### For Small Team
2. **Heroku** or **Docker on DigitalOcean** - Simple, affordable

### For Production
3. **AWS/Azure/GCP with Docker** - Scalable, enterprise-ready

---

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connection
4. Review security group rules
5. Consult platform-specific documentation

---

**Next Steps:**
1. Choose deployment platform
2. Follow platform-specific guide above
3. Complete post-deployment checklist
4. Test application thoroughly
5. Monitor and optimize

---

*Last updated: October 23, 2026*
