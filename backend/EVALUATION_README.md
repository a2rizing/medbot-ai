# Model Evaluation Guide

This guide explains how to evaluate your MedBot-AI pneumonia detection model and generate all necessary metrics and visualizations for your research paper.

## Quick Start

### On Windows (Local):
```cmd
cd backend
run_evaluation.bat
```

### On Linux/Mac or EC2:
```bash
cd backend
source venv/bin/activate  # Or: python3.11 -m venv venv && source venv/bin/activate
pip install torch torchvision numpy matplotlib seaborn scikit-learn pandas pillow tqdm
python evaluate_model.py
```

## What You'll Get

The evaluation script generates publication-ready visualizations and metrics:

### 📊 Visualizations (PNG files, 300 DPI):
1. **confusion_matrix.png** - Shows true positives, false positives, true negatives, false negatives
2. **roc_curve.png** - ROC curve with AUC score
3. **precision_recall_curve.png** - Precision-Recall curve with AUC
4. **metrics_bar_chart.png** - Bar chart comparing accuracy, precision, recall, F1-score

### 📄 Reports:
1. **classification_report.txt** - Detailed per-class metrics
2. **metrics.json** - All metrics in JSON format for easy parsing
3. **predictions.csv** - Per-image predictions with probabilities

## Input Requirements

You'll need to provide:

1. **Image directory**: Folder containing test images (JPG/PNG format)
   - Example: `../data/rsna/images`
   
2. **Labels CSV**: CSV file with columns:
   - `image`: Image filename (e.g., "patient123.jpg")
   - `label`: Ground truth label (0 = Normal, 1 = Pneumonia)

Example labels.csv:
```csv
image,label
patient001.jpg,0
patient002.jpg,1
patient003.jpg,1
```

## Metrics Explained

### Accuracy
- **What**: Percentage of correct predictions
- **Formula**: (TP + TN) / (TP + TN + FP + FN)
- **Good for**: Overall performance when classes are balanced

### Precision
- **What**: Of all predicted pneumonia cases, how many were actually pneumonia?
- **Formula**: TP / (TP + FP)
- **Good for**: Minimizing false alarms (false positives)

### Recall (Sensitivity)
- **What**: Of all actual pneumonia cases, how many did we detect?
- **Formula**: TP / (TP + FN)
- **Good for**: Ensuring we don't miss cases (minimize false negatives)

### F1-Score
- **What**: Harmonic mean of precision and recall
- **Formula**: 2 × (Precision × Recall) / (Precision + Recall)
- **Good for**: Balance between precision and recall

### ROC AUC
- **What**: Area Under the Receiver Operating Characteristic curve
- **Range**: 0 to 1 (higher is better, 0.5 = random)
- **Good for**: Overall model discrimination ability

### PR AUC
- **What**: Area Under the Precision-Recall curve
- **Good for**: Evaluating performance on imbalanced datasets

## Example Output

```
============================================================
RESULTS
============================================================
Accuracy:  0.9245
Precision: 0.8891
Recall:    0.9134
F1-Score:  0.9011

Total samples: 1000
Positive samples (Pneumonia): 487
Negative samples (Normal): 513
ROC AUC: 0.9612
PR AUC: 0.9523
============================================================
```

## Using Results in Your Paper

### For Methods Section:
- Model architecture: DenseNet-121
- Input size: 224×224
- Preprocessing: ImageNet normalization
- Device: CPU/GPU (check output)

### For Results Section:
Include the generated figures:
- Confusion matrix (Figure 1)
- ROC curve (Figure 2)
- PR curve (Figure 3)
- Metrics comparison (Figure 4)

### For Tables:
Use metrics from `metrics.json` or `classification_report.txt`

Example table:
| Metric | Score |
|--------|-------|
| Accuracy | 92.45% |
| Precision | 88.91% |
| Recall | 91.34% |
| F1-Score | 90.11% |
| ROC AUC | 96.12% |

## Troubleshooting

### "Model file not found"
- Ensure `densepneumo_ace.pt` is in the `backend/` directory
- Check the MODEL_PATH in `evaluate_model.py`

### "Image directory not found"
- Provide the full or relative path to your test images
- Example: `../data/rsna/images` or `C:/path/to/images`

### "Labels CSV not found"
- Ensure CSV has columns: `image`, `label`
- Labels should be 0 (Normal) or 1 (Pneumonia)

### Memory errors
- Reduce batch size in `evaluate_model.py` (line with `DataLoader`)
- Use CPU instead of GPU if RAM is limited

### Import errors
```bash
pip install torch torchvision numpy matplotlib seaborn scikit-learn pandas pillow tqdm
```

## Customization

To modify the evaluation:

1. **Change threshold**: Edit line in `evaluate_model.py`:
   ```python
   predictions = (probabilities >= 0.5).astype(int)  # Change 0.5
   ```

2. **Change batch size**: Edit DataLoader:
   ```python
   dataloader = DataLoader(dataset, batch_size=32, ...)  # Change 32
   ```

3. **Add more metrics**: Import from sklearn.metrics and add to `metrics_dict`

## Citation

If you use this evaluation framework in your research, please cite:

```bibtex
@software{medbot_eval,
  title={MedBot-AI Evaluation Framework},
  author={Your Name},
  year={2025},
  url={https://github.com/a2rizing/medbot-ai}
}
```

## Support

For issues or questions:
1. Check this README
2. Review the code comments in `evaluate_model.py`
3. Check AWS deployment guide for EC2 setup

---

**Happy Evaluating! 🎯**
