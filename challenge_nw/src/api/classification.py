import json
import logging
import os
from datetime import datetime
import pandas as pd
from pydantic import BaseModel

from fastapi import BackgroundTasks

from src.api import (
    app,
    OUTPUT_PATH,
    modelxgb,
    preprocessor,
)

logger = logging.getLogger(__name__)

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Request


def data_process(input_json):
    # calcular dia-I, mes-I y hora a partir de Fecha-I.
    # drop Fecha-I
    dia_i = input_json.FechaI.day
    mes_i = input_json.FechaI.month
    hora = input_json.FechaI.hour + input_json.FechaI.minute / 60
    input_json = json.loads(input_json.json())
    input_json["DiaI"] = dia_i
    input_json["MesI"] = mes_i
    input_json["Hora"] = hora
    del input_json["FechaI"]
    return input_json


def preprocessing(input_json):
    # mismo procesamiento que en el notebook.
    # se ocupa el mismo preprocessor que se fiteo con datos de train.
    df = pd.DataFrame.from_dict({k: [v] for k, v in input_json.items()})
    cols = [
        columna
        for cont, columna in enumerate(df.columns)
        if df.dtypes[cont] != "float64"
    ]
    df[cols] = df[cols].astype("category")
    df.columns = [
        "Ori-I",
        "Des-I",
        "Emp-I",
        "DIANOM",
        "TIPOVUELO",
        "DIA-I",
        "MES-I",
        "Hora",
    ]
    x_pred = preprocessor.transform(df)
    return x_pred


def get_prediction(data):
    input_json = data_process(data)
    x_pred = preprocessing(input_json)
    pred = modelxgb.predict_proba(x_pred)
    # aqui guardaria el valor en un archivo y lo subiria a AWS s3 usando boto3.
    # Implementaria un metodo 'get' para que el usuario pueda obtenerlo cuando esté listo.
    # No tengo acceso a AWS, no puedo hacerlo.
    return pred


class ClassificationRequest(BaseModel):
    FechaI: datetime
    OriI: str
    DesI: str
    EmpI: str
    DIANOM: str
    TIPOVUELO: str


class ClassificationRequestResponse(BaseModel):
    probabilidad: float


@app.post(
    "/predict",
    response_model=ClassificationRequestResponse,
    tags=["Probabilidad de atraso de vuelo"],
    summary="Solicitud de clasificación",
)
async def predict_request(
    data: ClassificationRequest, background_tasks: BackgroundTasks
):
    """
    Solicitud de clasificación
    """
    background_tasks.add_task(get_prediction, data)

    response = ClassificationRequestResponse(probabilidad=1)
    return response
