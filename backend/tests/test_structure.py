import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.feature_engineering.feature_builder import create_feature_builder

if __name__ == "__main__":
    builder = create_feature_builder()
    result = builder.build(23.2599, 77.4126)
    print("Structure test passed:", result)

