from app.forecasting.historical_loader import HistoricalDataLoader
from app.forecasting.time_feature_extractor import TimeFeatureExtractor
from app.forecasting.dataset_builder import DatasetBuilder
from app.forecasting.dataset_splitter import DatasetSplitter

from app.ml.random_forest_model import RandomForestModel
from app.ml.decision_tree_model import DecisionTreeModel
from app.ml.model_evaluator import ModelEvaluator
from app.ml.model_behavior_analyzer import ModelBehaviorAnalyzer


# -----------------------------
# Load Dataset
# -----------------------------
loader = HistoricalDataLoader(
    "datasets/nasa_power/solar_history.csv"
)

dataset = loader.get_dataset()

# -----------------------------
# Feature Engineering
# -----------------------------
extractor = TimeFeatureExtractor()

dataset = extractor.transform(dataset)

# -----------------------------
# Build Dataset
# -----------------------------
builder = DatasetBuilder(dataset)

X, y = builder.build_dataset()

# -----------------------------
# Split Dataset
# -----------------------------
splitter = DatasetSplitter()

split_data = splitter.split(X, y)

# -----------------------------
# Train Models
# -----------------------------
rf_model = RandomForestModel()

dt_model = DecisionTreeModel()

rf_result = rf_model.train(split_data)

dt_result = dt_model.train(split_data)

# -----------------------------
# Evaluate Models
# -----------------------------
evaluator = ModelEvaluator()

# Random Forest Training Metrics
rf_train_metrics = evaluator.evaluate(
    split_data["y_train"],
    rf_result["training_predictions"]
)

# Random Forest Validation Metrics
rf_validation_metrics = evaluator.evaluate(
    split_data["y_validation"],
    rf_result["validation_predictions"]
)

# Decision Tree Training Metrics
dt_train_metrics = evaluator.evaluate(
    split_data["y_train"],
    dt_result["training_predictions"]
)

# Decision Tree Validation Metrics
dt_validation_metrics = evaluator.evaluate(
    split_data["y_validation"],
    dt_result["validation_predictions"]
)

# -----------------------------
# Analyze Behaviour
# -----------------------------
analyzer = ModelBehaviorAnalyzer()

rf_behavior = analyzer.analyze(
    rf_train_metrics,
    rf_validation_metrics
)

dt_behavior = analyzer.analyze(
    dt_train_metrics,
    dt_validation_metrics
)

# -----------------------------
# Print Results
# -----------------------------
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print("\nRandom Forest")
print("Training Metrics")
print(rf_train_metrics)

print("Validation Metrics")
print(rf_validation_metrics)

print("Behaviour")
print(rf_behavior)

print("\n" + "-" * 60)

print("\nDecision Tree")
print("Training Metrics")
print(dt_train_metrics)

print("Validation Metrics")
print(dt_validation_metrics)

print("Behaviour")
print(dt_behavior)

print("\n" + "=" * 60)

# -----------------------------
# Best Model
# -----------------------------
if rf_validation_metrics["MAE"] < dt_validation_metrics["MAE"]:
    print("Best Model : Random Forest")
else:
    print("Best Model : Decision Tree")

print("=" * 60)