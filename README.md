# MedBot AI – Pneumonia Detection from Chest X-rays

**MedBot** is an AI-powered web application that detects pneumonia from X-ray scans using a deep learning model (DenseNet121).  
Users can upload images through a simple web interface and receive instant predictions with confidence scores.

## 🚀 Quick Start

1. **Setup Backend**: See [Quick Reference](QUICK_REFERENCE.md) or [Deployment Guide](AWS_DEPLOYMENT_GUIDE.md)
2. **Run Evaluation**: See [Evaluation Guide](backend/EVALUATION_README.md)
3. **Check Setup**: Run `python backend/check_setup.py`

## 📚 Documentation

- **[Quick Reference Card](QUICK_REFERENCE.md)** - Commands, troubleshooting, API endpoints
- **[AWS Deployment Guide](AWS_DEPLOYMENT_GUIDE.md)** - Complete EC2 + S3 deployment steps
- **[Evaluation Guide](backend/EVALUATION_README.md)** - Generate metrics and visualizations for research

## Tech Stack
- **Frontend:** React.js  
- **Backend:** FastAPI  
- **AI Model:** PyTorch (DenseNet121)  
- **Dataset:** RSNA Pneumonia Detection Challenge  
- **Deployment:** AWS EC2 + S3

## Features
- ✅ Upload X-ray images  
- ✅ Real-time pneumonia detection  
- ✅ Confidence scores  
- ✅ GPU/CPU acceleration  
- ✅ Grad-CAM heatmaps for visual explainability
- ✅ Comprehensive evaluation metrics (confusion matrix, ROC, PR curves)
- ✅ Production-ready deployment on AWS

## Project Structure
```bash
medbot-ai/
├── backend/
│   ├── main.py                   # FastAPI backend
│   ├── densepneumo_ace.pt       # Model weights (place here)
│   ├── evaluate_model.py        # Evaluation script
│   ├── check_setup.py           # Setup verification
│   └── requirements.txt         # Dependencies
├── frontend/
│   └── medbot-ui/               # React web interface
├── model/
│   ├── gradcam_utils.py         # Grad-CAM implementation
│   └── train_baseline.ipynb     # Training notebook
├── data/                        # Dataset (not in repo)
├── notebooks/                   # Analysis notebooks
├── AWS_DEPLOYMENT_GUIDE.md      # Full deployment guide
├── QUICK_REFERENCE.md           # Quick commands & tips
└── README.md                    # This file
```

## Getting Started

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/a2rizing/medbot-ai.git
cd medbot-ai/backend

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place model file
# Copy densepneumo_ace.pt to backend/

# 5. Run backend
uvicorn main:app --reload --port 8000

# 6. Access API
# Open http://localhost:8000
```

### AWS Deployment

See the complete [AWS Deployment Guide](AWS_DEPLOYMENT_GUIDE.md) for step-by-step instructions.

### Model Evaluation

```bash
cd backend
python evaluate_model.py
```

Generates publication-ready metrics and visualizations in `evaluation_results/`:
- Confusion matrix
- ROC curve with AUC
- Precision-Recall curve
- Classification report
- Metrics JSON and CSV

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Predict pneumonia from X-ray image
- `POST /gradcam` - Generate Grad-CAM heatmap visualization

See [Quick Reference](QUICK_REFERENCE.md#-api-endpoints) for detailed usage.

## Model Performance

Run evaluation to get current metrics. Example output:
- **Accuracy**: ~92%
- **Precision**: ~89%
- **Recall**: ~91%
- **F1-Score**: ~90%
- **ROC AUC**: ~96%

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Citation

If you use this project in your research, please cite:

```bibtex
@software{medbot_ai,
  title={MedBot-AI: Pneumonia Detection from Chest X-rays},
  author={Abhishek Arun Raja},
  year={2025},
  url={https://github.com/a2rizing/medbot-ai}
}
```

## Acknowledgments

- RSNA Pneumonia Detection Challenge for the dataset
- PyTorch and FastAPI communities
- DenseNet architecture authors

## Support

For issues or questions:
- Check the [Quick Reference](QUICK_REFERENCE.md)
- Review the [Deployment Guide](AWS_DEPLOYMENT_GUIDE.md)
- Open an issue on GitHub
