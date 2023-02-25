import logging
import joblib
import xgboost as xgb
from fastapi import FastAPI


# necesito un output_path
OUTPUT_PATH = "data/output"

modelxgb = xgb.XGBClassifier()
modelxgb.load_model("objects/model.json")
preprocessor = joblib.load("objects/preprocessor.joblib")

logger = logging.getLogger()
app = FastAPI(title="API Probabilidad de Atraso", docs_url="/docs")


def init():
    from src.api import classification


init()
