
import joblib

MODEL_PATH = "PAMU_BOAT/models/ai_model.pkl"

model = joblib.load(MODEL_PATH)

print("✅ AIモデル読込完了")
