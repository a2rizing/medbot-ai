# MedBot-AI AWS Deployment Guide

## Complete Step-by-Step AWS Deployment Instructions

This guide will walk you through deploying your MedBot-AI backend and frontend on AWS using EC2 and S3, staying within the free tier limits.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Part 1: EC2 Setup for Backend](#part-1-ec2-setup-for-backend)
3. [Part 2: Backend Deployment](#part-2-backend-deployment)
4. [Part 3: Frontend Deployment](#part-3-frontend-deployment)
5. [Part 4: Domain & SSL (Optional)](#part-4-domain--ssl-optional)
6. [Part 5: Testing & Troubleshooting](#part-5-testing--troubleshooting)

---

## Prerequisites

### What You Need:
- ✅ AWS account with free tier access
- ✅ Your .pem file (`medbot-key.pem`)
- ✅ MedBot-AI project code
- ✅ Model weights file (`densepneumo_ace.pt`)
- ✅ Basic command line knowledge

### Budget Estimate:
- EC2 t3.micro: **FREE** (750 hours/month)
- EBS 20GB: **FREE** (within 30GB limit)
- S3 for frontend: **~$0.50-1/month** (negligible for small site)
- Total: **Less than $2/month** (mostly free tier)

---

## Part 1: EC2 Setup for Backend

### Step 1.1: Verify/Launch EC2 Instance

1. **Log in to AWS Console**: https://console.aws.amazon.com/
2. **Navigate to EC2**: Search for "EC2" in the top search bar
3. **Check your instance**:
   - Go to "Instances" in the left sidebar
   - Make sure your instance is **running**
   - Note the **Public IPv4 address** (e.g., 51.20.87.3)

4. **Verify Security Group** (IMPORTANT):
   - Select your instance → "Security" tab → "Security groups"
   - Click on the security group name
   - Click "Edit inbound rules"
   - **Ensure these rules exist**:
     - **SSH**: Port 22, Source: Your IP or 0.0.0.0/0
     - **HTTP**: Port 80, Source: 0.0.0.0/0
     - **Custom TCP**: Port 8000, Source: 0.0.0.0/0 (for FastAPI)
   - Click "Save rules"

### Step 1.2: Increase EBS Volume (Already Done)

✅ You already increased to 20GB, but here's how to verify:
```bash
# After SSH into EC2:
df -h
# Should show ~18-20GB available on /dev/root or /dev/xvda1
```

If you need more space later:
1. EC2 Console → Volumes (left sidebar)
2. Select your volume → Actions → Modify Volume
3. Increase size → Modify
4. SSH into instance and run:
```bash
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1
df -h  # Verify new size
```

---

## Part 2: Backend Deployment

### Step 2.1: Connect to EC2

**On your local Windows PowerShell:**
```powershell
cd "C:\Users\ABHISHEK ARUN RAJA\Documents\Coding Projects\MedBot-AI"
ssh -i medbot-key.pem ubuntu@<YOUR-EC2-PUBLIC-IP>
```
Replace `<YOUR-EC2-PUBLIC-IP>` with your current public IP from AWS Console.

**If connection times out:**
- Verify instance is running
- Check public IP hasn't changed
- Verify security group allows SSH from your IP

### Step 2.2: Prepare EC2 Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 (for dependency compatibility)
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Install Git
sudo apt install -y git

# Install system dependencies for image processing
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

### Step 2.3: Upload Your Code to EC2

**Option A: Using Git (Recommended)**
```bash
# On EC2
cd ~
git clone https://github.com/a2rizing/medbot-ai.git
cd medbot-ai/backend
```

**Option B: Using SCP (if not using Git)**

On your **local PowerShell** (NOT on EC2):
```powershell
# Upload entire backend folder
scp -i medbot-key.pem -r "C:\Users\ABHISHEK ARUN RAJA\Documents\Coding Projects\MedBot-AI\medbot-ai\backend" ubuntu@<YOUR-EC2-IP>:~/
```

### Step 2.4: Set Up Python Environment

```bash
# Navigate to backend
cd ~/medbot-ai/backend  # Or ~/backend if you used SCP

# Create virtual environment with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Remove Windows-only package from requirements
sed -i '/pywinpty/d' requirements.txt

# Install dependencies (this may take 5-10 minutes)
pip install -r requirements.txt

# If you get space errors, install CPU-only PyTorch:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Step 2.5: Verify Model File

```bash
# Check if model file exists
ls -lh densepneumo_ace.pt

# If file is missing, upload it from local machine
# On local PowerShell:
# scp -i medbot-key.pem "path\to\densepneumo_ace.pt" ubuntu@<EC2-IP>:~/medbot-ai/backend/
```

### Step 2.6: Test Backend Locally on EC2

```bash
# Still in virtual environment (venv activated)
cd ~/medbot-ai/backend

# Run FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test from your local browser:**
- Open: `http://<YOUR-EC2-IP>:8000`
- You should see: `{"message": "MedBot backend loaded successfully."}`

Press `Ctrl+C` to stop the server.

### Step 2.7: Run Backend with Production Server (Gunicorn + Uvicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (production-ready)
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Step 2.8: Keep Backend Running (systemd service)

Create a systemd service to keep your backend running even after you disconnect:

```bash
# Create service file
sudo nano /etc/systemd/system/medbot.service
```

Paste this content (replace paths if needed):
```ini
[Unit]
Description=MedBot FastAPI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/medbot-ai/backend
Environment="PATH=/home/ubuntu/medbot-ai/backend/venv/bin"
ExecStart=/home/ubuntu/medbot-ai/backend/venv/bin/gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and exit: `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable medbot
sudo systemctl start medbot

# Check status
sudo systemctl status medbot

# View logs
sudo journalctl -u medbot -f
```

**Your backend is now running 24/7!**  
Access it at: `http://<YOUR-EC2-IP>:8000`

---

## Part 3: Frontend Deployment

You have two options for frontend deployment:

### Option A: Deploy on S3 + CloudFront (Recommended - Cheaper & Faster)

#### Step 3A.1: Build Frontend Locally

**On your local machine:**
```powershell
cd "C:\Users\ABHISHEK ARUN RAJA\Documents\Coding Projects\MedBot-AI\medbot-ai\frontend\medbot-ui"

# Install dependencies (if not already done)
npm install

# Update API endpoint to point to your EC2
# Edit src/api/config.js or wherever your API URL is defined
# Change: http://localhost:8000 → http://<YOUR-EC2-IP>:8000

# Build for production
npm run build
```

This creates a `build/` or `dist/` folder with static files.

#### Step 3A.2: Create S3 Bucket

1. **AWS Console** → Search "S3"
2. **Create bucket**:
   - Bucket name: `medbot-frontend` (must be globally unique)
   - Region: Same as your EC2 (e.g., eu-north-1)
   - **Uncheck** "Block all public access"
   - Acknowledge the warning
   - Create bucket

3. **Upload files**:
   - Open your bucket
   - Click "Upload"
   - Drag and drop all files from your `build/` folder
   - Click "Upload"

4. **Enable static website hosting**:
   - Bucket → Properties → Static website hosting
   - Enable
   - Index document: `index.html`
   - Error document: `index.html`
   - Save changes

5. **Set bucket policy** (make public):
   - Bucket → Permissions → Bucket policy
   - Paste this (replace `medbot-frontend` with your bucket name):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::medbot-frontend/*"
    }
  ]
}
```
   - Save

6. **Get website URL**:
   - Bucket → Properties → Static website hosting
   - Copy the "Bucket website endpoint" (e.g., http://medbot-frontend.s3-website.eu-north-1.amazonaws.com)

**Your website is now live!**

#### Step 3A.3: (Optional) Add CloudFront for HTTPS

1. **CloudFront Console** → Create Distribution
2. Origin domain: Select your S3 bucket website endpoint
3. Viewer protocol policy: Redirect HTTP to HTTPS
4. Default root object: `index.html`
5. Create distribution
6. Wait 10-15 minutes for deployment
7. Access via CloudFront domain (e.g., https://d123456.cloudfront.net)

---

### Option B: Serve Frontend from EC2 (Simpler, but less scalable)

```bash
# On EC2
cd ~/medbot-ai/frontend/medbot-ui

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install dependencies
npm install

# Build
npm run build

# Install serve
sudo npm install -g serve

# Serve on port 80 (requires sudo)
sudo serve -s build -l 80
```

Or set up Nginx:
```bash
sudo apt install -y nginx

# Copy build files
sudo cp -r build/* /var/www/html/

# Restart nginx
sudo systemctl restart nginx
```

Access at: `http://<YOUR-EC2-IP>`

---

## Part 4: Domain & SSL (Optional)

### Using Route 53 + Certificate Manager:

1. **Register domain** (Route 53 or external like Namecheap)
2. **Create hosted zone** in Route 53
3. **Request SSL certificate** in AWS Certificate Manager
4. **Point domain to**:
   - CloudFront distribution (for S3 frontend)
   - EC2 Elastic IP (for EC2 frontend)
5. **Update CloudFront** to use custom domain and SSL

---

## Part 5: Testing & Troubleshooting

### Test Backend:

```bash
# Check if backend is running
curl http://<YOUR-EC2-IP>:8000

# Test prediction (upload an X-ray image)
curl -X POST http://<YOUR-EC2-IP>:8000/predict \
  -F "file=@/path/to/xray.jpg"
```

### Test Frontend:

Open your browser:
- S3: `http://your-bucket-name.s3-website.region.amazonaws.com`
- EC2: `http://<YOUR-EC2-IP>`
- CloudFront: `https://your-cloudfront-domain.cloudfront.net`

### Common Issues:

**1. "Connection refused" or timeout:**
- Check security group allows the port
- Verify instance is running
- Check if service is running: `sudo systemctl status medbot`

**2. "No space left on device":**
```bash
# Clean up
sudo apt clean
rm -rf ~/.cache/pip
df -h  # Check space
```

**3. Backend not loading model:**
```bash
# Check model file exists
ls -lh ~/medbot-ai/backend/densepneumo_ace.pt

# Check logs
sudo journalctl -u medbot -n 50
```

**4. CORS errors in browser:**
- Verify backend allows frontend origin
- Check CORS settings in `main.py`

---

## Part 6: Run Model Evaluation

To generate confusion matrix and metrics for your journal:

```bash
# On EC2 or locally
cd ~/medbot-ai/backend
source venv/bin/activate

# Run evaluation script
python evaluate_model.py
```

Follow the prompts to provide:
- Path to test images
- Path to labels CSV

Results will be saved in `evaluation_results/`:
- `confusion_matrix.png`
- `roc_curve.png`
- `precision_recall_curve.png`
- `metrics_bar_chart.png`
- `classification_report.txt`
- `metrics.json`
- `predictions.csv`

**Download results to local machine:**
```powershell
# On local PowerShell
scp -i medbot-key.pem -r ubuntu@<EC2-IP>:~/medbot-ai/backend/evaluation_results ./
```

---

## Cost Monitoring

1. **AWS Console** → Billing Dashboard
2. Set up **billing alerts**:
   - CloudWatch → Alarms → Create alarm
   - Billing metric → Estimated charges
   - Set threshold (e.g., $5)

3. **Monitor free tier usage**:
   - Billing → Free Tier

---

## Summary Checklist

- [ ] EC2 instance running with 20GB storage
- [ ] Security groups allow ports 22, 80, 8000
- [ ] Python 3.11 installed
- [ ] Backend code uploaded
- [ ] Dependencies installed (without pywinpty)
- [ ] Model file (`densepneumo_ace.pt`) in place
- [ ] Backend running as systemd service
- [ ] Backend accessible at http://<EC2-IP>:8000
- [ ] Frontend built and deployed (S3 or EC2)
- [ ] Frontend can communicate with backend
- [ ] Model evaluation completed with metrics
- [ ] Billing alerts set up

---

## Next Steps

1. **Test thoroughly** with real X-ray images
2. **Generate evaluation metrics** for your journal paper
3. **Set up monitoring** (CloudWatch for logs)
4. **Consider adding**:
   - Database for storing predictions
   - User authentication
   - Rate limiting
   - Backup strategy

---

## Support

If you encounter issues:
1. Check logs: `sudo journalctl -u medbot -f`
2. Verify security groups and network settings
3. Test locally on EC2 first before exposing publicly

**Estimated total time**: 1-2 hours
**Estimated monthly cost**: $0-2 (mostly free tier)

Good luck with your deployment! 🚀
