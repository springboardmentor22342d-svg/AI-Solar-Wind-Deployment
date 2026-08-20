import sys
import os

# Add the backend directory to sys.path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.analysis_pipeline import AnalysisPipeline
from app.schemas.analysis import AnalysisResponse

def test_pipeline():
    pipeline = AnalysisPipeline()

    locations = [
        {"name": "Thar Desert, Rajasthan (Solar Ideal)", "lat": 26.9, "lon": 71.3},
        {"name": "Kanyakumari (Wind Ideal)", "lat": 8.08, "lon": 77.53},
        {"name": "Leh, Ladakh (High Altitude / Cold)", "lat": 34.15, "lon": 77.57},
        {"name": "Mumbai City (Urban / Constrained)", "lat": 19.07, "lon": 72.87},
        {"name": "Gujarat Coast (Hybrid Potential)", "lat": 22.25, "lon": 68.96}
    ]
    
    passed = 0
    
    for loc in locations:
        print(f"\n--- Testing Location: {loc['name']} ({loc['lat']}, {loc['lon']}) ---")
        try:
            result = pipeline.execute_pipeline(loc['lat'], loc['lon'], site_name=loc['name'])
            
            # Validate against Pydantic schema
            AnalysisResponse(**result)
            
            print(f"PASS: Execution successful.")
            print(f"   ML Score: {result['evaluation']['overall_score']}")
            print(f"   Feasible: {result['technical_feasibility']['is_feasible']}")
            print(f"   Recommendation: {result['deployment']['recommended_technology']}")
            
            if result.get("energy_yield"):
                print(f"   Energy Yield: {result['energy_yield']['total_energy_mwh']} MWh")
            if result.get("financial_metrics"):
                print(f"   ROI: {result['financial_metrics']['roi']}%")
                
            passed += 1
            
        except Exception as e:
            print(f"FAIL: Execution failed: {e}")
            import traceback
            traceback.print_exc()
            
    print(f"\nCompleted {passed}/{len(locations)} tests successfully.")

if __name__ == "__main__":
    test_pipeline()
