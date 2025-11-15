# 🚀 PCOS Predictor - Deployment Guide

Complete guide to deploying your PCOS Predictor application to production.

---

## 📋 Table of Contents

1. [Deployment Options](#deployment-options)
2. [Free Hosting Options](#free-hosting-options)
3. [Recommended: Render.com (Free)](#option-1-rendercom-easiest-free)
4. [Alternative: Railway.app](#option-2-railwayapp)
5. [Alternative: Heroku](#option-3-heroku)
6. [Self-Hosting on VPS](#option-4-vps-self-hosting)
7. [Pre-Deployment Checklist](#pre-deployment-checklist)
8. [Post-Deployment Steps](#post-deployment-steps)

---

## 🌐 Deployment Options

### Free Hosting (Best for Students/Personal Projects)
- ✅ **Render.com** - Recommended, generous free tier
- ✅ **Railway.app** - Easy deployment, free trial
- ✅ **Vercel (Frontend)** + **Render (Backend)** - Split deployment
- ✅ **Heroku** - Classic option (limited free tier)

### Paid Hosting (Production/Commercial)
- 💰 **AWS (Elastic Beanstalk)** - $10-50/month
- 💰 **DigitalOcean App Platform** - $5-20/month
- 💰 **Google Cloud Platform** - $10-30/month
- 💰 **Azure Web Apps** - $10-40/month

---

## 🆓 Free Hosting Options

### Quick Comparison

| Platform | Backend | Database | Frontend | Free Tier Limits |
|----------|---------|----------|----------|------------------|
| **Render.com** | ✅ | ✅ PostgreSQL | ✅ | 750 hrs/month, sleeps after 15 min |
| **Railway.app** | ✅ | ✅ PostgreSQL | ✅ | $5 credit/month, then paid |
| **Vercel** | ❌ | ❌ | ✅ | Unlimited, great for React |
| **Netlify** | ❌ | ❌ | ✅ | Unlimited, static hosting |
| **Heroku** | ✅ | ✅ | ✅ | Limited hours, sleeps after 30 min |

---

## 🎯 Option 1: Render.com (Easiest, Free)

**✨ Recommended for beginners - completely free tier!**

### Step 1: Prepare Your Project

1. **Create a GitHub repository**
   ```bash
   cd "c:\Users\vyahu\Downloads\PCOS-iomp\PCOS-rp\PCOS-rp"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/PCOS-predictor.git
   git push -u origin main
   ```

2. **Create `render.yaml` in project root**
   ```yaml
   services:
     # Backend service
     - type: web
       name: pcos-backend
       env: python
       buildCommand: "cd backend && pip install -r requirements.txt"
       startCommand: "cd backend && gunicorn app:app"
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
         - key: SECRET_KEY
           generateValue: true
         - key: DB_HOST
           fromDatabase:
             name: pcos-db
             property: host
         - key: DB_NAME
           fromDatabase:
             name: pcos-db
             property: database
         - key: DB_USER
           fromDatabase:
             name: pcos-db
             property: user
         - key: DB_PASSWORD
           fromDatabase:
             name: pcos-db
             property: password
         - key: DB_PORT
           fromDatabase:
             name: pcos-db
             property: port

     # Frontend service
     - type: web
       name: pcos-frontend
       env: static
       buildCommand: "cd frontend && npm install && npm run build"
       staticPublishPath: frontend/build
       envVars:
         - key: REACT_APP_API_URL
           value: https://pcos-backend.onrender.com

   databases:
     - name: pcos-db
       databaseName: pcos_db
       user: pcos_user
   ```

3. **Update `backend/requirements.txt` - Add Gunicorn**
   ```txt
   flask
   flask-cors
   psycopg2-binary
   scikit-learn
   joblib
   numpy
   pandas
   pyjwt
   werkzeug
   gunicorn
   ```

4. **Create `backend/wsgi.py`**
   ```python
   from app import app

   if __name__ == "__main__":
       app.run()
   ```

### Step 2: Deploy on Render

1. **Sign up at [render.com](https://render.com)**
   - Use GitHub account for easy connection

2. **Create PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Name: `pcos-db`
   - Free tier (expires after 90 days, but can create new one)
   - Note down the connection details

3. **Deploy Backend**
   - Dashboard → New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Name**: `pcos-backend`
     - **Environment**: Python 3
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
     - **Environment Variables**: Add all from render.yaml
   - Click "Create Web Service"

4. **Deploy Frontend**
   - Dashboard → New → Static Site
   - Connect same GitHub repository
   - Settings:
     - **Name**: `pcos-frontend`
     - **Build Command**: `cd frontend && npm install && npm run build`
     - **Publish Directory**: `frontend/build`
     - **Environment Variables**:
       - `REACT_APP_API_URL` = `https://pcos-backend.onrender.com`
   - Click "Create Static Site"

5. **Initialize Database**
   - Go to your PostgreSQL database dashboard
   - Click "Connect" → "External Connection"
   - Use psql or pgAdmin to run `database_setup.sql`

### Step 3: Update Frontend Config

**Update `frontend/src/config.js`**:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export default API_BASE_URL;
```

### Step 4: Update Backend CORS

**Update `backend/app.py` CORS settings**:
```python
CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000",
    "https://pcos-frontend.onrender.com",  # Add your Render frontend URL
    "https://YOUR-CUSTOM-DOMAIN.com"  # If you have a custom domain
])
```

---

## 🚂 Option 2: Railway.app

**Railway is super easy but has limited free credits.**

### Step 1: Prepare Project

1. **Create `Procfile` in backend folder**
   ```
   web: gunicorn app:app
   ```

2. **Create `railway.json` in project root**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "cd backend && gunicorn app:app",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

### Step 2: Deploy

1. **Sign up at [railway.app](https://railway.app)**
2. **New Project → Deploy from GitHub**
3. **Add PostgreSQL**:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway auto-creates DATABASE_URL
4. **Add Backend Service**:
   - Click "New" → "GitHub Repo"
   - Select your repo
   - Set environment variables
5. **Add Frontend**:
   - New service from same repo
   - Set build command: `cd frontend && npm install && npm run build`
   - Set start command: `npx serve -s frontend/build`

---

## 🌊 Option 3: Heroku

**Heroku recently limited its free tier, but still an option.**

### Quick Deploy

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku Apps**
   ```bash
   # Backend
   heroku create pcos-backend
   heroku addons:create heroku-postgresql:mini
   
   # Frontend
   heroku create pcos-frontend --buildpack mars/create-react-app
   ```

3. **Deploy**
   ```bash
   # Backend
   cd backend
   git init
   heroku git:remote -a pcos-backend
   git add .
   git commit -m "Deploy"
   git push heroku main
   
   # Frontend
   cd ../frontend
   git init
   heroku git:remote -a pcos-frontend
   git add .
   git commit -m "Deploy"
   git push heroku main
   ```

---

## 🖥️ Option 4: VPS Self-Hosting

**For more control - requires Linux knowledge.**

### Providers:
- DigitalOcean Droplet - $5/month
- AWS EC2 - $3-10/month
- Linode - $5/month
- Vultr - $5/month

### Quick Setup (Ubuntu 22.04)

```bash
# 1. SSH into your server
ssh root@YOUR_SERVER_IP

# 2. Update system
apt update && apt upgrade -y

# 3. Install dependencies
apt install -y python3 python3-pip python3-venv postgresql nodejs npm nginx

# 4. Clone your project
git clone https://github.com/YOUR_USERNAME/PCOS-predictor.git
cd PCOS-predictor

# 5. Setup database
sudo -u postgres psql -f database_setup.sql

# 6. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/pcos-backend.service
```

**Backend service file**:
```ini
[Unit]
Description=PCOS Backend
After=network.target

[Service]
User=root
WorkingDirectory=/root/PCOS-predictor/backend
Environment="PATH=/root/PCOS-predictor/backend/venv/bin"
ExecStart=/root/PCOS-predictor/backend/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Start backend
sudo systemctl start pcos-backend
sudo systemctl enable pcos-backend

# 7. Setup frontend
cd ../frontend
npm install
npm run build

# 8. Setup Nginx
sudo nano /etc/nginx/sites-available/pcos
```

**Nginx config**:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    # Frontend
    location / {
        root /root/PCOS-predictor/frontend/build;
        try_files $uri /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/pcos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL (optional but recommended)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d YOUR_DOMAIN
```

---

## ✅ Pre-Deployment Checklist

Before deploying, make sure:

### Backend
- [ ] `gunicorn` added to `requirements.txt`
- [ ] `SECRET_KEY` uses environment variable
- [ ] Database config uses environment variables
- [ ] CORS configured for production domain
- [ ] `.env` file in `.gitignore`
- [ ] All ML model `.pkl` files committed to repo
- [ ] Error handling and logging implemented
- [ ] Database initialization works automatically

### Frontend
- [ ] `config.js` uses environment variable for API URL
- [ ] Build command works: `npm run build`
- [ ] No hardcoded localhost URLs
- [ ] All dependencies in `package.json`
- [ ] Production build tested locally

### Database
- [ ] `database_setup.sql` is up to date
- [ ] Can be run multiple times safely (IF NOT EXISTS)
- [ ] Migrations strategy planned
- [ ] Backup strategy planned

### Security
- [ ] Strong SECRET_KEY generated
- [ ] Database password is strong
- [ ] HTTPS configured
- [ ] CORS properly restricted
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] Rate limiting considered

---

## 🔧 Configuration Files Needed

### 1. `.gitignore` (Project Root)
```
# Python
backend/__pycache__/
backend/venv/
backend/.env
*.pyc
*.pyo
*.pyd

# Node
frontend/node_modules/
frontend/build/
frontend/.env.local

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

### 2. `backend/.env.example`
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=pcos_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_PORT=5432

# Security
SECRET_KEY=change-this-to-a-random-long-string

# Environment
FLASK_ENV=production
```

### 3. `backend/Procfile` (for Heroku/Railway)
```
web: gunicorn app:app
```

---

## 📊 Environment Variables Setup

### For Render/Railway/Heroku:

**Backend Environment Variables:**
```
SECRET_KEY=<random-string-here>
DB_HOST=<provided-by-platform>
DB_NAME=pcos_db
DB_USER=<provided-by-platform>
DB_PASSWORD=<provided-by-platform>
DB_PORT=5432
PYTHON_VERSION=3.11.0
```

**Frontend Environment Variables:**
```
REACT_APP_API_URL=https://your-backend-url.com
```

---

## 🚀 Post-Deployment Steps

### 1. Test Your Deployment

```bash
# Test backend health
curl https://your-backend.com/health

# Test frontend
# Open https://your-frontend.com in browser

# Test registration
curl -X POST https://your-backend.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","full_name":"Test User"}'
```

### 2. Monitor Your Application

- Set up logging (use platform's built-in logs)
- Monitor database usage
- Track API response times
- Set up uptime monitoring (UptimeRobot.com - free)

### 3. Setup Custom Domain (Optional)

1. Buy domain from Namecheap, GoDaddy, etc. ($10/year)
2. Add DNS records:
   - Frontend: CNAME to platform's URL
   - Backend: CNAME to platform's URL
3. Configure SSL certificate (usually automatic)

### 4. Regular Maintenance

- [ ] Backup database weekly
- [ ] Monitor error logs
- [ ] Update dependencies monthly
- [ ] Review security alerts
- [ ] Test all features after updates

---

## 🆘 Troubleshooting

### "Application Error" or "Service Unavailable"

**Check:**
1. Build logs - any errors during build?
2. Environment variables - all set correctly?
3. Database connection - is DB running?
4. Start command - correct?

**Fix:**
```bash
# Check logs on Render
render logs -s YOUR_SERVICE_NAME

# Check logs on Railway
railway logs

# Check logs on Heroku
heroku logs --tail -a YOUR_APP_NAME
```

### CORS Errors

**Update backend CORS settings**:
```python
CORS(app, supports_credentials=True, origins=[
    "https://your-frontend-domain.com",
    "http://localhost:3000"  # For local testing
])
```

### Database Connection Failed

**Check:**
1. Database is running and accessible
2. Environment variables match database credentials
3. Firewall allows connections
4. SSL mode if required

### Model Files Not Found

**Ensure all `.pkl` files are in repo**:
```bash
git add backend/*.pkl
git commit -m "Add ML model files"
git push
```

---

## 💡 Best Practices

1. **Use Environment Variables** - Never hardcode secrets
2. **Enable HTTPS** - Always use SSL in production
3. **Implement Rate Limiting** - Prevent abuse
4. **Setup Monitoring** - Know when things break
5. **Regular Backups** - Export database weekly
6. **Version Control** - Tag releases, use branches
7. **Error Handling** - Graceful errors, don't expose internals
8. **Documentation** - Keep deployment docs updated

---

## 🎯 Recommended: Start with Render

**For your project, I recommend Render.com because:**

✅ Completely free tier  
✅ Easy PostgreSQL setup  
✅ Automatic HTTPS  
✅ GitHub integration  
✅ Good documentation  
✅ No credit card required  

**Deployment time:** ~30 minutes  
**Cost:** $0 (free tier)

---

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don't_Do_This)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/latest/deploying/)

---

## ✨ You're Ready to Deploy!

Choose a platform above and follow the steps. Start with Render for the easiest free option!

**Good luck with your deployment! 🚀**
