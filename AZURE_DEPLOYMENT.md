# 🚀 Deploy Study Pal to Azure App Service

This guide will help you deploy your Study Pal application to Microsoft Azure, making it accessible worldwide with a custom domain and professional hosting.

## 📋 Prerequisites

1. **Azure Account**: [Create a free Azure account](https://azure.microsoft.com/free/) (includes $200 credit)
2. **Azure CLI**: [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Git**: Ensure Git is installed for deployment
4. **DeepSeek API Key**: Your API key for AI quiz generation

## 🎯 Deployment Options

### Option 1: Deploy via Azure Portal (Recommended for Beginners)

#### Step 1: Create App Service
1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"**
3. Search for **"Web App"** and select it
4. Click **"Create"**

#### Step 2: Configure Basic Settings
```
Resource Group: Create new → "study-pal-rg"
Name: your-unique-app-name (e.g., "study-pal-2024")
Publish: Code
Runtime stack: Python 3.11
Operating System: Linux
Region: East US (or closest to your users)
```

#### Step 3: Choose Pricing Plan
- **Development**: Free F1 (good for testing)
- **Production**: Basic B1 or Standard S1 (recommended)
- **High Traffic**: Premium P1V2 or higher

#### Step 4: Review and Create
1. Click **"Review + create"**
2. Click **"Create"**
3. Wait 2-3 minutes for deployment

### Option 2: Deploy via Azure CLI (Advanced)

```bash
# Login to Azure
az login

# Create resource group
az group create --name study-pal-rg --location eastus

# Create App Service plan
az appservice plan create --name study-pal-plan --resource-group study-pal-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group study-pal-rg --plan study-pal-plan --name your-unique-app-name --runtime "PYTHON|3.11"
```

## 🔧 Configure Application Settings

### Step 1: Set Environment Variables
1. Go to your App Service in Azure Portal
2. Navigate to **Configuration** → **Application settings**
3. Add these settings:

```
Name: DEEPSEEK_API_KEY
Value: your-actual-deepseek-api-key

Name: SCM_DO_BUILD_DURING_DEPLOYMENT
Value: true

Name: WEBSITES_ENABLE_APP_SERVICE_STORAGE
Value: true
```

### Step 2: Configure Python Version
1. In **Configuration** → **General settings**
2. Set **Python version** to **3.11**
3. Set **Startup command** to: `python startup.py`

## 📁 Prepare Your Code for Deployment

### Required Files (Already Created)
- ✅ `startup.py` - Azure App Service entry point
- ✅ `web.config` - IIS configuration for routing
- ✅ `.deployment` - Deployment configuration
- ✅ `requirements.txt` - Python dependencies

### File Structure
```
study-pal/
├── app.py                 # Main Flask application
├── startup.py            # Azure entry point
├── web.config            # IIS configuration
├── .deployment           # Deployment config
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── questions.csv         # Sample questions
├── static/               # CSS, JS, images
├── templates/            # HTML templates
└── uploads/              # PDF upload directory
```

## 🌐 Deploy Your Application

### Method 1: GitHub Integration (Recommended)

#### Step 1: Push to GitHub
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit for Azure deployment"

# Create GitHub repository and push
gh repo create study-pal --public
git branch -M main
git remote add origin https://github.com/yourusername/study-pal.git
git push -u origin main
```

#### Step 2: Connect Azure to GitHub
1. In Azure Portal, go to your App Service
2. Navigate to **Deployment Center**
3. Choose **GitHub** as source
4. Authorize Azure to access your GitHub
5. Select your **organization**, **repository**, and **branch**
6. Click **Save**

### Method 2: Local Git Deployment

#### Step 1: Configure Local Git
1. In Azure Portal, go to **Deployment Center**
2. Choose **Local Git**
3. Click **Save**
4. Copy the **Git Clone URL**

#### Step 2: Deploy via Git
```bash
# Add Azure remote
git remote add azure https://your-app-name.scm.azurewebsites.net:443/your-app-name.git

# Deploy to Azure
git push azure main
```

### Method 3: ZIP Deployment

```bash
# Create deployment package
zip -r study-pal.zip . -x "*.git*" "*.env" "__pycache__/*" "*.pyc"

# Deploy via Azure CLI
az webapp deployment source config-zip --resource-group study-pal-rg --name your-app-name --src study-pal.zip
```

## 🔒 Security Configuration

### Step 1: Enable HTTPS
1. Go to **Custom domains** in Azure Portal
2. Turn on **HTTPS Only**
3. Configure **TLS/SSL settings**

### Step 2: Configure CORS (if needed)
1. Navigate to **CORS** in Azure Portal
2. Add allowed origins:
   - `https://your-domain.com`
   - `https://www.your-domain.com`

### Step 3: Set Up Custom Domain (Optional)
1. Purchase a domain from any registrar
2. In Azure Portal, go to **Custom domains**
3. Add your domain and configure DNS records

## 📊 Monitoring and Scaling

### Application Insights
1. Go to **Application Insights** in Azure Portal
2. Create new instance or connect existing
3. Enable monitoring for performance tracking

### Auto-scaling
1. Navigate to **Scale out (App Service plan)**
2. Enable **Autoscale**
3. Configure rules based on:
   - CPU percentage
   - Memory usage
   - Request count

## 🗄️ Database Considerations

Your app currently uses JSON files for data storage. For production, consider:

### Option 1: Keep File Storage (Simple)
- Files will persist in Azure App Service
- Good for small to medium usage
- No additional cost

### Option 2: Upgrade to Azure Database (Recommended for Production)
- **Azure Database for PostgreSQL**
- **Azure Cosmos DB**
- Better performance and reliability

## 🚀 Post-Deployment Steps

### Step 1: Test Your Application
1. Visit `https://your-app-name.azurewebsites.net`
2. Test all features:
   - ✅ Home page loads
   - ✅ PDF upload works
   - ✅ Quiz generation functions
   - ✅ Quiz taking works
   - ✅ History tracking works

### Step 2: Upload Initial Content
1. Upload a sample CSV file with questions
2. Test PDF upload with a small document
3. Verify AI quiz generation works

### Step 3: Configure Backup
1. Go to **Backups** in Azure Portal
2. Configure automated backups
3. Set retention policy

## 💰 Cost Optimization

### Pricing Tiers
- **Free F1**: $0/month (1GB storage, 60 CPU minutes/day)
- **Basic B1**: ~$13/month (10GB storage, unlimited compute)
- **Standard S1**: ~$56/month (50GB storage, auto-scaling)

### Cost-Saving Tips
1. **Use Free Tier** for development/testing
2. **Scale down** during low usage periods
3. **Monitor usage** with Azure Cost Management
4. **Set spending alerts** to avoid surprises

## 🔧 Troubleshooting

### Common Issues

#### 1. Application Won't Start
**Problem**: App shows "Application Error"
**Solution**: 
- Check Application Insights logs
- Verify `startup.py` is configured correctly
- Check Python version matches requirements

#### 2. Static Files Not Loading
**Problem**: CSS/JS files return 404
**Solution**:
- Verify `web.config` is present
- Check static file paths in templates
- Enable static file serving in App Service

#### 3. Environment Variables Not Working
**Problem**: DeepSeek API key not found
**Solution**:
- Verify environment variables in Azure Configuration
- Restart the application
- Check variable names match code

#### 4. File Upload Issues
**Problem**: PDF uploads fail
**Solution**:
- Check file size limits in Azure (default 100MB)
- Verify upload directory permissions
- Monitor disk space usage

### Logs and Debugging
```bash
# View live logs
az webapp log tail --name your-app-name --resource-group study-pal-rg

# Download logs
az webapp log download --name your-app-name --resource-group study-pal-rg
```

## 🌟 Advanced Features

### Custom Domain Setup
1. Purchase domain from registrar
2. Add CNAME record: `your-app-name.azurewebsites.net`
3. Configure SSL certificate in Azure

### CDN Integration
1. Create Azure CDN profile
2. Configure endpoint for static files
3. Update templates to use CDN URLs

### Database Migration
```python
# Example: Migrate to PostgreSQL
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
```

## 📞 Support and Resources

- **Azure Documentation**: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)
- **Azure Support**: Available in Azure Portal
- **Community**: [Stack Overflow - Azure](https://stackoverflow.com/questions/tagged/azure)
- **Pricing Calculator**: [azure.microsoft.com/pricing/calculator](https://azure.microsoft.com/pricing/calculator)

## 🎉 Congratulations!

Your Study Pal application is now live on Azure! 🚀

**Next Steps**:
1. Share your app URL with users
2. Monitor performance and usage
3. Collect user feedback
4. Plan future enhancements

---

**Your live application URL**: `https://your-app-name.azurewebsites.net`

Happy learning! 📚✨ 