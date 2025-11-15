why# 🚀 Quick Deploy - PCOS Predictor

Choose your deployment platform:

## ⚡ Fastest: Render.com (Recommended)

**Time:** 15 minutes | **Cost:** Free

1. **Push to GitHub** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin https://github.com/YOUR_USERNAME/PCOS-predictor.git
   git push -u origin main
   ```

2. **Go to [render.com](https://render.com)** and sign up with GitHub

3. **Deploy with Blueprint** (Easiest!)
   - Click "New" → "Blueprint"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml` and deploy everything!
   - Wait ~5 minutes for deployment

4. **Initialize Database**
   - Click on your PostgreSQL database
   - Click "Connect" → Copy the External Database URL
   - Use psql or pgAdmin to run:
     ```bash
     psql YOUR_DATABASE_URL -f database_setup.sql
     ```

5. **Update Frontend API URL**
   - Go to your frontend service settings
   - Update `REACT_APP_API_URL` environment variable to your backend URL
   - Example: `https://pcos-backend.onrender.com`
   - Trigger manual deploy

**Done! Your app is live! 🎉**

---

## 🚂 Alternative: Railway.app

**Time:** 10 minutes | **Cost:** $5 credit free, then paid

1. **Push to GitHub** (same as above)

2. **Go to [railway.app](https://railway.app)** and sign up

3. **New Project → Deploy from GitHub**
   - Select your repository

4. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway auto-creates `DATABASE_URL`

5. **Add Backend Service**
   - Settings → Environment
   - Add variables:
     - `SECRET_KEY` = (generate random string)
     - Use Railway's PostgreSQL variables for DB connection
   - Deploy

6. **Add Frontend Service**
   - New → GitHub Repo (same repo)
   - Settings:
     - Build Command: `cd frontend && npm install && npm run build`
     - Start Command: `cd frontend && npx serve -s build`
   - Environment:
     - `REACT_APP_API_URL` = (your backend Railway URL)

**Done! 🚂**

---

## 📊 After Deployment Checklist

- [ ] Backend health check works: `https://your-backend/health`
- [ ] Frontend loads without errors
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Lifestyle assessment works
- [ ] Symptom tracker works
- [ ] History page shows assessments
- [ ] No CORS errors in browser console

---

## 🆘 Common Issues

### "Application Error"
→ Check build logs, ensure all environment variables are set

### CORS Error
→ Update backend CORS to include your frontend URL

### Database Connection Failed
→ Verify all DB environment variables match your database

### Model Files Not Found
→ Ensure all `.pkl` files are committed to Git

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` for detailed instructions, troubleshooting, and alternative platforms.

---

**Need help?** Check the deployment guide or the troubleshooting section!
