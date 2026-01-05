# AIVerse Backend - Deployment Guide

## 🚀 Quick Comparison: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| **Free Tier** | $5 credit/month (limited) | 750 hours/month free |
| **PostgreSQL** | ✅ Built-in | ✅ Built-in |
| **Deploy Speed** | Fast (30-60s) | Slower (2-5 min) |
| **Custom Domain** | ✅ Free | ✅ Free |
| **Auto-deploy** | ✅ GitHub integration | ✅ GitHub integration |
| **Sleep on Inactivity** | No | Yes (free tier) |
| **Best For** | Quick deploys, hobby projects | Free hosting needs |

### **Recommendation: Railway** 
Railway is better because:
- Faster deployments
- No cold starts (your API won't sleep)
- Better developer experience
- Easy environment variable management

---

## 📦 Pre-deployment Checklist

1. ✅ Production settings configured
2. ✅ `requirements.txt` with production dependencies
3. ✅ `Procfile` for gunicorn
4. ✅ `runtime.txt` for Python version
5. ✅ `.gitignore` configured

---

## 🚂 Option A: Deploy to Railway (Recommended)

### Step 1: Create GitHub Repository

```bash
# Navigate to the backend deploy folder
cd aiverse-backend-deploy

# Initialize git
git init
git add .
git commit -m "Initial commit - AIVerse backend"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/aiverse-backend.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `aiverse-backend` repository
4. Railway will auto-detect it's a Python/Django project

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway automatically sets `DATABASE_URL` environment variable

### Step 4: Set Environment Variables

In Railway dashboard → Your service → **Variables** tab, add:

```
SECRET_KEY=your-super-secret-key-generate-a-random-one
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
FRONTEND_URL=https://your-frontend.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Generate a secure SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

Railway auto-deploys when you push to GitHub. Your API will be at:
```
https://your-app.up.railway.app/api/
```

---

## 🎨 Option B: Deploy to Render

### Step 1: Create GitHub Repository
Same as Railway Step 1

### Step 2: Create Web Service on Render

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name:** aiverse-backend
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn aiverse_api.wsgi:application`

### Step 3: Add PostgreSQL Database

1. Go to **"New"** → **"PostgreSQL"**
2. Copy the **Internal Database URL**
3. Add it as `DATABASE_URL` in your web service environment

### Step 4: Set Environment Variables

In Render dashboard → Your service → **Environment** tab, add:

```
SECRET_KEY=your-super-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
FRONTEND_URL=https://your-frontend.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
DATABASE_URL=<your-postgres-internal-url>
PYTHON_VERSION=3.11.7
```

### Step 5: Deploy

Click **"Manual Deploy"** or push to GitHub for auto-deploy.

---

## 🔗 Connecting Frontend to Backend

After deploying, update your Vercel frontend:

### Option 1: Environment Variable (Recommended)

1. Go to your Vercel dashboard → Project → **Settings** → **Environment Variables**
2. Add:
   ```
   VITE_API_URL=https://your-backend.up.railway.app
   ```

3. Update your frontend `src/lib/api.ts`:

```typescript
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";
export const IMAGE_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/media/` 
  : "/media/";

// ... rest of the file
```

### Option 2: Direct URL Update

Update `src/lib/api.ts`:

```typescript
const API_BASE_URL = "https://your-backend.up.railway.app/api";
export const IMAGE_BASE_URL = "https://your-backend.up.railway.app/media/";
```

### Update vite.config.ts (Remove Proxy)

Since you're no longer using a local backend, update your Vite config:

```typescript
export default defineConfig({
  plugins: [react()],
  // Remove or comment out the proxy section for production
  // server: {
  //   proxy: { ... }
  // }
});
```

---

## 📝 Post-Deployment Steps

### 1. Run Migrations

Railway automatically runs migrations via Procfile. For Render:
```bash
# In Render Shell or via SSH
python manage.py migrate
```

### 2. Create Superuser

```bash
# Access shell in Railway/Render
python manage.py createsuperuser
```

### 3. Test Your API

```bash
# Test health check
curl https://your-backend.up.railway.app/api/events/

# Test admin panel
https://your-backend.up.railway.app/admin/
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Make sure `FRONTEND_URL` and `CORS_ALLOWED_ORIGINS` match your Vercel URL exactly (include https://)

2. **Database Connection Failed**
   - Verify `DATABASE_URL` is set correctly
   - Railway sets this automatically when you add PostgreSQL

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic` (Railway does this via Procfile)

4. **500 Errors**
   - Check logs in Railway/Render dashboard
   - Make sure `DEBUG=False` and `SECRET_KEY` is set

---

## 📊 Your URLs After Deployment

- **Backend API:** `https://your-app.up.railway.app/api/`
- **Admin Panel:** `https://your-app.up.railway.app/admin/`
- **Media Files:** `https://your-app.up.railway.app/media/`
- **Frontend:** `https://your-frontend.vercel.app`

---

## 💡 Pro Tips

1. **Use Custom Domains:** Both Railway and Render support free custom domains
2. **Monitor Logs:** Check deployment logs for errors
3. **Database Backups:** Railway and Render offer database backups
4. **Environment Separation:** Use different env vars for staging/production
