"""
Model Evaluation Script for MedBot-AI
Generates confusion matrix, ROC curve, precision-recall curve, and other metrics
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, 
    classification_report, 
    roc_curve, 
    auc, 
    precision_recall_curve,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
import pandas as pd
import os
from tqdm import tqdm
import json

# Configuration
MODEL_PATH = "densepneumo_ace.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
OUTPUT_DIR = "evaluation_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Image preprocessing (same as inference)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


class PneumoniaDataset(Dataset):
    """Dataset for loading pneumonia images with labels"""
    def __init__(self, image_dir, labels_csv, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        
        # Load labels
        self.data = pd.read_csv(labels_csv)
        print(f"Loaded {len(self.data)} samples from {labels_csv}")
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        img_name = self.data.iloc[idx]['image']
        img_path = os.path.join(self.image_dir, img_name)
        label = self.data.iloc[idx]['label']
        
        # Load image
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
            
        return image, label, img_name


def load_model(model_path, device):
    """Load the trained DenseNet121 model"""
    model = models.densenet121(pretrained=False)
    model.classifier = nn.Linear(model.classifier.in_features, 1)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model


def evaluate_model(model, dataloader, device):
    """Run inference and collect predictions"""
    all_labels = []
    all_predictions = []
    all_probabilities = []
    all_filenames = []
    
    print("Running model evaluation...")
    with torch.no_grad():
        for images, labels, filenames in tqdm(dataloader):
            images = images.to(device)
            outputs = model(images)
            probabilities = torch.sigmoid(outputs).cpu().numpy().flatten()
            predictions = (probabilities >= 0.5).astype(int)
            
            all_labels.extend(labels.numpy())
            all_predictions.extend(predictions)
            all_probabilities.extend(probabilities)
            all_filenames.extend(filenames)
    
    return np.array(all_labels), np.array(all_predictions), np.array(all_probabilities), all_filenames


def plot_confusion_matrix(y_true, y_pred, output_path):
    """Generate and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Pneumonia'],
                yticklabels=['Normal', 'Pneumonia'])
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {output_path}")
    
    return cm


def plot_roc_curve(y_true, y_proba, output_path):
    """Generate and save ROC curve"""
    fpr, tpr, thresholds = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"ROC curve saved to {output_path}")
    
    return roc_auc


def plot_precision_recall_curve(y_true, y_proba, output_path):
    """Generate and save Precision-Recall curve"""
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    pr_auc = auc(recall, precision)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2, label=f'PR curve (AUC = {pr_auc:.3f})')
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve', fontsize=16, fontweight='bold')
    plt.legend(loc="lower left")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Precision-Recall curve saved to {output_path}")
    
    return pr_auc


def plot_metrics_bar(metrics_dict, output_path):
    """Generate bar chart of key metrics"""
    plt.figure(figsize=(10, 6))
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [
        metrics_dict['accuracy'],
        metrics_dict['precision'],
        metrics_dict['recall'],
        metrics_dict['f1_score']
    ]
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    bars = plt.bar(metrics, values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.3f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylim([0, 1.1])
    plt.ylabel('Score', fontsize=12)
    plt.title('Model Performance Metrics', fontsize=16, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Metrics bar chart saved to {output_path}")


def save_classification_report(y_true, y_pred, output_path):
    """Save detailed classification report"""
    report = classification_report(y_true, y_pred, 
                                   target_names=['Normal', 'Pneumonia'],
                                   digits=4)
    
    with open(output_path, 'w') as f:
        f.write("Classification Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)
    
    print(f"Classification report saved to {output_path}")


def save_metrics_json(metrics_dict, output_path):
    """Save metrics as JSON for easy parsing"""
    with open(output_path, 'w') as f:
        json.dump(metrics_dict, f, indent=4)
    
    print(f"Metrics JSON saved to {output_path}")


def save_predictions_csv(filenames, y_true, y_pred, y_proba, output_path):
    """Save detailed predictions to CSV"""
    df = pd.DataFrame({
        'filename': filenames,
        'true_label': y_true,
        'predicted_label': y_pred,
        'probability': y_proba,
        'correct': y_true == y_pred
    })
    df.to_csv(output_path, index=False)
    print(f"Predictions CSV saved to {output_path}")


def main():
    """Main evaluation pipeline"""
    print("=" * 60)
    print("MedBot-AI Model Evaluation")
    print("=" * 60)
    print(f"Device: {DEVICE}")
    print(f"Model: {MODEL_PATH}")
    print()
    
    # Prompt for dataset path
    print("Please provide the path to your test dataset:")
    print("Example: ../data/rsna/images")
    image_dir = input("Image directory: ").strip()
    
    print("\nPlease provide the path to your labels CSV:")
    print("Example: ../data/rsna/labels.csv")
    labels_csv = input("Labels CSV: ").strip()
    
    if not os.path.exists(image_dir):
        print(f"Error: Image directory not found: {image_dir}")
        return
    
    if not os.path.exists(labels_csv):
        print(f"Error: Labels CSV not found: {labels_csv}")
        return
    
    print()
    
    # Load model
    print("Loading model...")
    model = load_model(MODEL_PATH, DEVICE)
    print("Model loaded successfully!")
    print()
    
    # Create dataset and dataloader
    print("Loading dataset...")
    dataset = PneumoniaDataset(image_dir, labels_csv, transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=0)
    print()
    
    # Evaluate
    y_true, y_pred, y_proba, filenames = evaluate_model(model, dataloader, DEVICE)
    
    # Calculate metrics
    print("\nCalculating metrics...")
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    metrics_dict = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'total_samples': len(y_true),
        'positive_samples': int(np.sum(y_true)),
        'negative_samples': int(len(y_true) - np.sum(y_true))
    }
    
    # Print metrics
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print()
    
    # Generate visualizations
    print("Generating visualizations...")
    cm = plot_confusion_matrix(y_true, y_pred, 
                               os.path.join(OUTPUT_DIR, 'confusion_matrix.png'))
    
    roc_auc = plot_roc_curve(y_true, y_proba, 
                            os.path.join(OUTPUT_DIR, 'roc_curve.png'))
    metrics_dict['roc_auc'] = float(roc_auc)
    
    pr_auc = plot_precision_recall_curve(y_true, y_proba, 
                                        os.path.join(OUTPUT_DIR, 'precision_recall_curve.png'))
    metrics_dict['pr_auc'] = float(pr_auc)
    
    plot_metrics_bar(metrics_dict, 
                    os.path.join(OUTPUT_DIR, 'metrics_bar_chart.png'))
    
    # Save reports
    print("\nSaving reports...")
    save_classification_report(y_true, y_pred, 
                              os.path.join(OUTPUT_DIR, 'classification_report.txt'))
    
    save_metrics_json(metrics_dict, 
                     os.path.join(OUTPUT_DIR, 'metrics.json'))
    
    save_predictions_csv(filenames, y_true, y_pred, y_proba,
                        os.path.join(OUTPUT_DIR, 'predictions.csv'))
    
    print("\n" + "=" * 60)
    print("Evaluation complete!")
    print(f"All results saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
