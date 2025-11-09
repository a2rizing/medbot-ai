# AWS Deployment Checklist

Use this checklist to ensure you've completed all deployment steps correctly.

## Pre-Deployment

### Local Setup
- [ ] Model file (`densepneumo_ace.pt`) is in `backend/` directory
- [ ] All dependencies install successfully
- [ ] Backend runs locally without errors (`uvicorn main:app`)
- [ ] Can access http://localhost:8000
- [ ] Prediction endpoint works with test image
- [ ] Evaluation completed successfully
- [ ] Frontend builds without errors (`npm run build`)

### AWS Account
- [ ] AWS account created and verified
- [ ] Payment method added
- [ ] Free tier eligible
- [ ] Billing alerts set up ($5 threshold recommended)

## EC2 Setup

### Instance Configuration
- [ ] EC2 instance launched (t3.micro or t2.micro)
- [ ] Instance is in "running" state
- [ ] Public IPv4 address noted: ________________
- [ ] Key pair (.pem file) downloaded and secured
- [ ] EBS volume increased to 20GB
- [ ] File system resized (`df -h` shows ~20GB)

### Security Group
- [ ] SSH (port 22) - Source: Your IP or 0.0.0.0/0
- [ ] HTTP (port 80) - Source: 0.0.0.0/0
- [ ] Custom TCP (port 8000) - Source: 0.0.0.0/0
- [ ] Security group rules saved

### SSH Access
- [ ] Can connect via SSH: `ssh -i medbot-key.pem ubuntu@<EC2-IP>`
- [ ] No connection timeout errors
- [ ] SSH key permissions correct (400 on Linux/Mac)

## Backend Deployment

### System Setup
- [ ] System updated (`sudo apt update && sudo apt upgrade`)
- [ ] Python 3.11 installed
- [ ] Git installed
- [ ] System dependencies installed (libgl1-mesa-glx, libglib2.0-0)

### Code Deployment
- [ ] Code uploaded to EC2 (via Git or SCP)
- [ ] In correct directory (`cd ~/medbot-ai/backend`)
- [ ] Model file uploaded (`ls -lh densepneumo_ace.pt` shows file)
- [ ] Virtual environment created with Python 3.11
- [ ] Virtual environment activated
- [ ] `pywinpty` removed from requirements.txt
- [ ] All dependencies installed successfully

### Backend Testing
- [ ] Backend runs without errors
- [ ] Can access http://<EC2-IP>:8000 from browser
- [ ] Root endpoint returns success message
- [ ] Prediction endpoint tested with sample image
- [ ] Grad-CAM endpoint works (if applicable)
- [ ] Logs directory created
- [ ] Predictions logged correctly

### Production Setup
- [ ] Gunicorn installed
- [ ] Backend runs with Gunicorn
- [ ] Systemd service created (`/etc/systemd/system/medbot.service`)
- [ ] Service enabled (`sudo systemctl enable medbot`)
- [ ] Service started (`sudo systemctl start medbot`)
- [ ] Service status is "active (running)"
- [ ] Backend auto-starts after reboot (test by rebooting)
- [ ] Logs accessible (`sudo journalctl -u medbot -f`)

## Frontend Deployment

### Option A: S3 + CloudFront
- [ ] Frontend API endpoint updated to EC2 IP
- [ ] Frontend built successfully (`npm run build`)
- [ ] S3 bucket created (globally unique name)
- [ ] Static website hosting enabled
- [ ] Build files uploaded to S3
- [ ] Bucket policy set for public read access
- [ ] Website endpoint works (http://bucket.s3-website.region.amazonaws.com)
- [ ] CloudFront distribution created (optional)
- [ ] CloudFront distribution deployed
- [ ] HTTPS works via CloudFront (optional)

### Option B: EC2 (Nginx)
- [ ] Node.js installed on EC2
- [ ] Frontend code uploaded
- [ ] Dependencies installed (`npm install`)
- [ ] Frontend built (`npm run build`)
- [ ] Nginx installed
- [ ] Build files copied to `/var/www/html/`
- [ ] Nginx restarted
- [ ] Can access frontend via http://<EC2-IP>

## Testing

### Backend Tests
- [ ] Health check: `curl http://<EC2-IP>:8000`
- [ ] Prediction endpoint tested from local machine
- [ ] Response time acceptable (<5 seconds)
- [ ] Error handling works (test with invalid input)
- [ ] CORS allows frontend origin

### Frontend Tests
- [ ] Frontend loads in browser
- [ ] Can upload images
- [ ] Predictions display correctly
- [ ] Error messages show for invalid uploads
- [ ] UI is responsive
- [ ] No CORS errors in browser console

### Integration Tests
- [ ] Frontend successfully calls backend
- [ ] Predictions return to frontend
- [ ] Confidence scores display correctly
- [ ] Multiple predictions work in sequence

## Monitoring & Maintenance

### Monitoring Setup
- [ ] CloudWatch logs enabled (optional)
- [ ] Billing alerts configured
- [ ] Free tier usage checked
- [ ] Disk space monitored (`df -h`)
- [ ] Service status monitored

### Documentation
- [ ] EC2 public IP documented
- [ ] S3 bucket name documented (if used)
- [ ] CloudFront domain documented (if used)
- [ ] All credentials secured (not in code)
- [ ] Deployment notes written

## Security

### Basic Security
- [ ] SSH security group restricted to your IP (recommended)
- [ ] .pem file permissions set correctly
- [ ] No credentials in code or Git
- [ ] AWS access keys not exposed
- [ ] Security updates applied

### Optional Security Enhancements
- [ ] HTTPS enabled via CloudFront
- [ ] SSL certificate obtained
- [ ] Custom domain configured
- [ ] Rate limiting implemented
- [ ] API authentication added (for production)

## Evaluation & Metrics

### Model Evaluation
- [ ] Evaluation script runs successfully
- [ ] Confusion matrix generated
- [ ] ROC curve generated
- [ ] Precision-Recall curve generated
- [ ] Metrics bar chart generated
- [ ] Classification report generated
- [ ] All files downloaded from EC2

### Journal Paper Preparation
- [ ] All figures saved (300 DPI)
- [ ] Metrics documented
- [ ] Architecture diagram created
- [ ] Results table prepared
- [ ] Methodology documented

## Cost Management

### Free Tier Verification
- [ ] Instance is free-tier eligible (t2/t3.micro)
- [ ] Total EBS storage < 30GB
- [ ] Monitoring free tier usage
- [ ] No unexpected charges

### Optimization
- [ ] Instance stopped when not in use
- [ ] Old snapshots deleted
- [ ] Unused volumes removed
- [ ] S3 lifecycle policies set (optional)

## Final Checks

- [ ] All endpoints accessible from internet
- [ ] System stable for 24 hours
- [ ] No errors in logs
- [ ] Performance acceptable
- [ ] Backup plan in place
- [ ] Documentation complete
- [ ] Ready for demo/presentation

## Troubleshooting Completed

If any issues occurred, document solutions:

### Issue 1:
- **Problem**: ________________________________
- **Solution**: ________________________________

### Issue 2:
- **Problem**: ________________________________
- **Solution**: ________________________________

### Issue 3:
- **Problem**: ________________________________
- **Solution**: ________________________________

## Sign-Off

- **Deployment Date**: _______________
- **Deployed By**: _______________
- **Backend URL**: _______________
- **Frontend URL**: _______________
- **Status**: ⬜ Development  ⬜ Testing  ⬜ Production

## Notes

_Any additional notes or observations:_

---

**Next Steps After Deployment:**
1. Monitor for 48 hours
2. Test with real users
3. Gather feedback
4. Optimize performance
5. Plan for scaling (if needed)

**For Support:**
- Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Review [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)
- Check logs: `sudo journalctl -u medbot -f`

---

✅ **Deployment Complete!** 🎉
