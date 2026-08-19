from app.ml.feature_importance import FeatureImportance

importance = FeatureImportance()

ranking = importance.get_feature_importance()

print()

print("="*50)

print("FEATURE IMPORTANCE")

print("="*50)

for item in ranking:

    print(
        item["feature"],
        " : ",
        item["importance"]
    )