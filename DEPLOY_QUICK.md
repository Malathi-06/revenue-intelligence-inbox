# Quick Deployment Guide - Revenue Intelligence Inbox

## ⚡ Fastest Deployment: Streamlit Cloud (5 minutes)

### Prerequisites
- GitHub account
- Code pushed to GitHub repository

### Steps

#### 1. Commit and Push to GitHub
```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial deployment: Revenue Intelligence Inbox"

# Create GitHub repo and push
# Option A: Using GitHub CLI (recommended)
gh repo create revenue-intelligence-inbox --public --source=. --remote=origin
git push -u origin main

# Option B: Manual (if gh CLI not available)
# - Go to https://github.com/new
# - Create repository named "revenue-intelligence-inbox"
# - Follow instructions to push existing repository
```

#### 2. Deploy to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "Sign in" → Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository:** Select `yourusername/revenue-intelligence-inbox`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click "Deploy!"

#### 3. Wait for Deployment (2-3 minutes)
- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Run your application
  - Provide a public URL

#### 4. Your App is Live! 🎉
- URL: `https://yourusername-revenue-intelligence-inbox.streamlit.app`
- Share this URL with your team

### Optional: Configure Secrets (for PostgreSQL)
If using PostgreSQL instead of SQLite:

1. In Streamlit Cloud dashboard, click on your app
2. Click "Settings" → "Secrets"
3. Add your secrets in TOML format:
```toml
[database]
url = "postgresql://user:password@host:5432/dbname"
```
4. Update `src/utils/config.py` to read from secrets:
```python
import streamlit as st
DATABASE_URL = st.secrets.get("database", {}).get("url", "sqlite:///data/revenue.db")
```

---

## 🐳 Docker Deployment (10 minutes)

Perfect if you have Docker installed and want to run locally or on any cloud.

### Steps

#### 1. Build and Run with Docker Compose
```bash
# Build and start all services (app + PostgreSQL)
docker-compose up -d

# Wait for services to start (~30 seconds)

# Initialize database with synthetic data
docker-compose exec app python init_db.py

# View logs
docker-compose logs -f app

# Access application
# Open: http://localhost:8501
```

#### 2. Stop Services
```bash
docker-compose down

# To remove volumes (database data):
docker-compose down -v
```

---

## 🚀 Heroku Deployment (15 minutes)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli

### Steps

#### 1. Login and Create App
```bash
# Login to Heroku
heroku login

# Create app
heroku create revenue-intelligence-inbox

# Add PostgreSQL (optional, uses free tier)
heroku addons:create heroku-postgresql:mini
```

#### 2. Deploy
```bash
# Commit changes
git add .
git commit -m "Deploy to Heroku"

# Push to Heroku
git push heroku main

# Initialize database
heroku run python init_db.py

# Open application
heroku open
```

#### 3. View Logs
```bash
heroku logs --tail
```

---

## 🏢 AWS EC2 (30 minutes)

For production deployments with more control.

### Quick Setup

#### 1. Launch EC2 Instance
- AMI: Ubuntu 22.04
- Instance type: t2.small or larger
- Security group: Allow port 8501 (or 80/443)

#### 2. Connect and Install
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git
git clone https://github.com/yourusername/revenue-intelligence-inbox.git
cd revenue-intelligence-inbox
pip3 install -r requirements.txt

# Run application
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

#### 3. Keep Running (with tmux or systemd)
```bash
# Option A: Using tmux
tmux new -s streamlit
streamlit run app.py
# Press Ctrl+B then D to detach

# Option B: Using systemd (see DEPLOYMENT.md for full config)
sudo systemctl enable revenue-intelligence
sudo systemctl start revenue-intelligence
```

---

## 🔍 Verify Deployment

After deploying, verify these features:

### 1. Dashboard
- [ ] KPIs display correctly
- [ ] Charts render properly
- [ ] Date filter works

### 2. Inbox
- [ ] Conversations load
- [ ] Search works
- [ ] Can edit conversations

### 3. Routing
- [ ] View conflicts
- [ ] See routing explanations
- [ ] Audit log displays

### 4. Import/Export
- [ ] Can upload CSV
- [ ] Preview shows data
- [ ] Export downloads ZIP

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8501
kill -9 <PID>
```

### Database Connection Error
```bash
# Verify DATABASE_URL is set correctly
echo $DATABASE_URL  # Linux/Mac
echo %DATABASE_URL%  # Windows

# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('your-db-url'); print(engine.connect())"
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Deployment Fails
- Check logs: `heroku logs --tail` (Heroku) or `docker-compose logs` (Docker)
- Verify `requirements.txt` is complete
- Ensure Python version matches (3.11)

---

## 📱 Share Your Deployment

### Get Your URL
- **Streamlit Cloud:** `https://yourusername-revenue-intelligence-inbox.streamlit.app`
- **Heroku:** `https://revenue-intelligence-inbox.herokuapp.com`
- **Custom Domain:** Configure DNS and SSL certificate

### Demo Credentials (if you add auth)
- Username: `demo@example.com`
- Password: `demo123`

---

## 🎯 Next Steps After Deployment

1. **Replace Synthetic Data**
   - Connect to production CRM
   - Import real conversations
   - Update account and owner data

2. **Add Authentication**
   - Implement user login
   - Add role-based access control
   - Secure sensitive data

3. **Configure Monitoring**
   - Set up error tracking (Sentry)
   - Enable performance monitoring
   - Configure uptime alerts

4. **Optimize Performance**
   - Add caching with `@st.cache_data`
   - Optimize database queries
   - Enable CDN for static assets

5. **Backup Database**
   - Configure automated backups
   - Test restore procedure
   - Document recovery process

---

## 📊 Deployment Comparison

| Platform | Time | Cost | Difficulty | Best For |
|----------|------|------|------------|----------|
| **Streamlit Cloud** | 5 min | Free | ⭐ Easy | Demos, POCs |
| **Docker Local** | 10 min | Free | ⭐⭐ Medium | Development |
| **Heroku** | 15 min | $7/mo | ⭐⭐ Medium | Small teams |
| **AWS EC2** | 30 min | $20/mo | ⭐⭐⭐ Hard | Production |

---

## ✅ Deployment Checklist

Before going live:
- [ ] Code pushed to GitHub
- [ ] Database initialized
- [ ] Environment variables configured
- [ ] All tests passing (43/43)
- [ ] Application accessible via URL
- [ ] All features verified
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Documentation updated
- [ ] Team notified

---

**Need Help?**
- Full deployment guide: See `DEPLOYMENT.md`
- Architecture details: See `ARCHITECTURE.md`
- Quick start: See `QUICKSTART.md`

---

*Ready to deploy! Choose your platform above and follow the steps.* 🚀
