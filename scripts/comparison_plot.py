"""
Model Comparison Visualization Script
This script creates a bar chart comparing the performance of CNN and VGG16 models.
The plot shows training and validation accuracy for both models.
"""
import matplotlib.pyplot as plt
import os

# Get project root and results directory
scripts_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(scripts_dir)
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok=True)

# Model performance data
models = ['Baseline CNN', 'VGG16']
train_acc = [0.39, 0.89]
val_acc = [0.27, 0.72]

# Create comparison plot
x = range(len(models))
plt.bar(x, train_acc, width=0.4, label='Train Acc', align='center')
plt.bar(x, val_acc, width=0.4, label='Val Acc', align='edge')

plt.xticks(x, models)
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.title("CNN vs VGG16 Accuracy Comparison")
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save plot to results directory
output_path = os.path.join(results_dir, "comparison.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Comparison plot saved to: {output_path}")

# Optionally display the plot
# plt.show()
plt.close()
