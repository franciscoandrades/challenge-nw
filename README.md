<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Tabla de Contenidos**

- [Challenge-NW](#challenge-nw)
  - [Instalación](#instalaci%C3%B3n)
  - [API](#api)
    - [Endpoints](#endpoints)
  - [Pruebas de estrés](#pruebas-de-estr%C3%A9s)
    - [Resultado](#resultado)
    - [Cómo mejorar la API:](#c%C3%B3mo-mejorar-la-api)
  - [Para disponibilizar el modelo](#para-disponibilizar-el-modelo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Challenge-NW
Challenge for the NeuralWorks application

Pasos implementados:

  1. En **notebooks/to_expose.ipynb** agregué mejoras y opiniones al final del notebook, correr este notebook genera los archivos guardados en **objects/**.
  2. En **src/api** están los scripts pertinentes a la api.


## Instalación

- Instalar requisitos con `pip install -r requirements.txt`
- `Python 3.8`
- Para desarrollo, ejecutar `pre-commit install`.

## API

Tecnología: FastApi

Ejecutar `uvicorn src.api:app` dentro de la carpeta challenge_nw para levantar la API (en puerto 8000).

### Endpoints

Los endpoints disponibles son:
- `/docs`: Documentación de la API.

- `/predict`: POST. Predecir la probabilidad de atraso de un vuelo.
El endpoint recibe como parámetros:

  1. FechaI: Fecha Programada del vuelo.
  2. OriI: Ciudad origen.
  3. DesI: Ciudad destino.
  4. EmpI: Código Aerolínea.
  5. DIANOM: Dia de la semana programado.
  6. TIPOVUELO: Nacional o Internacional.

  - Ejemplo de payload: {
    "FechaI": "2023-02-25T06:16:24.077Z",
    "OriI": "string",
    "DesI": "string",
    "EmpI": "string",
    "DIANOM": "string",
    "TIPOVUELO": "string"
  }

  Disclaimer: El endpoint es async. Como no tengo acceso a cloud, termino no retornando nada. El método debería subir el resultado a una bd.


## Pruebas de estrés

cmd = ./wrk -c50000 -d45s http://127.0.0.1:8000/predict -s scripts/post.lua

En post.lua se debiése agregar:

wrk.method = "POST"

wrk.body = '{"FechaI": "2023-02-25T05:26:24.547Z","OriI": "string","DesI": "string","EmpI": "string","DIANOM": "string", "TIPOVUELO": "string"}'

wrk.headers["Content-Type"] = "application/json"

### Resultado

Running 45s test @ http://127.0.0.1:8000/predict
  2 threads and 50000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.81s    87.46ms   1.94s    54.90%
    Req/Sec   165.62    146.47   454.00     52.67%
  2412 requests in 45.08s, 341.54KB read
  Socket errors: connect 49749, read 21400, write 1, timeout 1922
Requests/sec:     53.50
Transfer/sec:      7.58KB

### Cómo mejorar la API:
  - Lo más directo: Ocupar una máquina con más recursos, mi computador no tiene muchos.
  - Encolamiento y paralelismo con celery y rabbitmq

## Para disponibilizar el modelo

Montar API en EC2 y habilitar el puerto pertinente.
