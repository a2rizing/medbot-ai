# MedBot-AI Quick Reference Card

## 🚀 Quick Commands

### Local Development (Windows)
```powershell
# Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload --port 8000

# Run evaluation
python evaluate_model.py

# Check setup
python check_setup.py
```

### AWS EC2 Deployment
```bash
# Connect
ssh -i medbot-key.pem ubuntu@<EC2-IP>

# Setup
cd ~/medbot-ai/backend
python3.11 -m venv venv
source venv/bin/activate
sed -i '/pywinpty/d' requirements.txt
pip install -r requirements.txt

# Run backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with Gunicorn (production)
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Run as service
sudo systemctl start medbot
sudo systemctl status medbot
sudo journalctl -u medbot -f
```

## 📁 File Structure
```
medbot-ai/
├── backend/
│   ├── main.py                    # FastAPI backend
│   ├── densepneumo_ace.pt        # Model weights (ADD THIS)
│   ├── evaluate_model.py         # Evaluation script
│   ├── check_setup.py            # Setup verification
│   ├── requirements.txt          # Dependencies
│   ├── logs/                     # Prediction logs
│   └── evaluation_results/       # Metrics & graphs
├── frontend/
│   └── medbot-ui/
│       ├── src/
│       ├── public/
│       └── package.json
├── model/
│   ├── gradcam_utils.py
│   └── dataset.py
├── data/
│   └── stage_2_test_images/
├── AWS_DEPLOYMENT_GUIDE.md       # Full deployment guide
└── README.md
```

## 🔌 API Endpoints

### GET /
- **Description**: Health check
- **Response**: `{"message": "MedBot backend loaded successfully."}`
- **Example**: `curl http://localhost:8000`

### POST /predict
- **Description**: Predict pneumonia from X-ray
- **Input**: Image file (multipart/form-data)
- **Response**: 
  ```json
  {
    "prediction": "Pneumonia Detected",
    "confidence": 0.8532
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/predict \
    -F "file=@xray.jpg"
  ```

### POST /gradcam
- **Description**: Generate Grad-CAM heatmap
- **Input**: Image file
- **Response**: PNG image with heatmap overlay
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/gradcam \
    -F "file=@xray.jpg" \
    --output gradcam_result.png
  ```

## 🎯 Evaluation Outputs

### Files Generated:
- `confusion_matrix.png` - TP, FP, TN, FN visualization
- `roc_curve.png` - ROC curve with AUC
- `precision_recall_curve.png` - PR curve with AUC
- `metrics_bar_chart.png` - Accuracy, Precision, Recall, F1
- `classification_report.txt` - Detailed per-class metrics
- `metrics.json` - All metrics in JSON format
- `predictions.csv` - Per-image predictions

### Key Metrics:
- **Accuracy**: Overall correctness
- **Precision**: True pneumonia / Predicted pneumonia
- **Recall**: Detected pneumonia / Actual pneumonia
- **F1-Score**: Harmonic mean of precision & recall
- **ROC AUC**: Model discrimination ability (0-1)
- **PR AUC**: Performance on imbalanced data

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout (SSH) | Check EC2 is running, verify public IP, check security group |
| Port already in use | Kill process: `lsof -ti:8000 \| xargs kill -9` (Linux) or `netstat -ano \| findstr :8000` (Windows) |
| Module not found | Activate venv: `source venv/bin/activate` or `venv\Scripts\activate` |
| Model file not found | Place `densepneumo_ace.pt` in backend directory |
| No space left | `sudo apt clean`, `rm -rf ~/.cache/pip`, increase EBS volume |
| CORS errors | Add frontend URL to CORS origins in `main.py` |
| pywinpty error (EC2) | Remove from requirements: `sed -i '/pywinpty/d' requirements.txt` |

## 📊 AWS Resources

### EC2 Security Group Rules:
| Type | Port | Source | Purpose |
|------|------|--------|---------|
| SSH | 22 | Your IP / 0.0.0.0/0 | Remote access |
| HTTP | 80 | 0.0.0.0/0 | Web traffic |
| Custom TCP | 8000 | 0.0.0.0/0 | FastAPI backend |

### Cost Optimization:
- ✅ t3.micro: FREE (750 hrs/month)
- ✅ EBS 20-30GB: FREE (within 30GB limit)
- ✅ S3 first 5GB: FREE
- ⚠️ Stop instance when not in use to save hours
- ⚠️ Set billing alerts at $5 threshold

## 🔒 Security Best Practices

1. **Restrict SSH**: Change security group source from 0.0.0.0/0 to your IP
2. **Use HTTPS**: Set up CloudFront with SSL certificate
3. **Environment variables**: Store sensitive data in .env files (not in Git)
4. **Keep updated**: `sudo apt update && sudo apt upgrade -y`
5. **Backup**: Save model weights and data to S3 regularly

## 📝 Environment Variables

Create `.env` file (don't commit to Git):
```env
MODEL_PATH=densepneumo_ace.pt
DEVICE=cpu
LOG_DIR=logs
FRONTEND_URL=http://localhost:3000
```

Load in `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🚦 Status Checks

```bash
# Check if backend is running
curl http://localhost:8000

# Check systemd service (EC2)
sudo systemctl status medbot

# View logs (EC2)
sudo journalctl -u medbot -f

# Check disk space
df -h

# Check memory
free -h

# Check port usage
lsof -i :8000  # Linux
netstat -ano | findstr :8000  # Windows
```

## 📞 Support Resources

- **AWS Documentation**: https://docs.aws.amazon.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **PyTorch Docs**: https://pytorch.org/docs/
- **Your Full Guide**: `AWS_DEPLOYMENT_GUIDE.md`
- **Evaluation Guide**: `EVALUATION_README.md`

## 🎓 For Your Journal Paper

Include:
1. Confusion matrix from `evaluation_results/`
2. ROC curve with AUC score
3. Classification report metrics
4. System architecture diagram (frontend → backend → model)
5. Deployment details (AWS EC2, FastAPI, DenseNet-121)

---

**Quick Start Checklist:**
- [ ] Model file in place (`densepneumo_ace.pt`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend running (`uvicorn main:app`)
- [ ] Can access http://localhost:8000
- [ ] Evaluation completed (`python evaluate_model.py`)
- [ ] Results ready for paper

**Deployment Checklist:**
- [ ] EC2 instance running with 20GB storage
- [ ] Security groups configured (ports 22, 80, 8000)
- [ ] Code uploaded to EC2
- [ ] Python 3.11 + venv set up
- [ ] Backend running as systemd service
- [ ] Frontend deployed (S3 or EC2)
- [ ] Billing alerts set up

---

*Last updated: November 2025*
