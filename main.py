import os
from typing import Union

import pandas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scenario_db = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/scenarios")
def list_scenarios():
    load_scenarios()
    print(scenario_db)
    return list(scenario_db.values())


@app.get("/scenarios/{id}")
def list_scenarios(id):
    load_scenarios()
    print(scenario_db)
    print(scenario_db.get(id))
    return scenario_db.get(id)


def load_scenarios():
    global scenario_db
    if len(scenario_db) != 0:
        return
    scenario_files = [
        filename for filename in os.listdir("./data") if filename.endswith(".csv")
    ]
    scenario_db = {
        scenario.replace(".csv", ""): format_scenario(scenario)
        for i, scenario in enumerate(scenario_files)
    }


def format_scenario(scenario_csv):
    df = pandas.read_csv(f"data/{scenario_csv}", header=None)
    print(df)
    print(df[df[0] == "Electricity|Imports"].squeeze()[1:])
    name = scenario_csv.replace(".csv", "")
    return {
        "key": name,
        "name": f"Scenario {name}",
        "co2": df[df[0] == "CO2|Total"].squeeze().iloc[1],
        "cost": df[df[0] == "Costs|System cost"].squeeze().iloc[1],
        "domestic": pandas.to_numeric(
            df[df[0] == "Electricity|Imports"].squeeze()[1:], errors="ignore"
        ).sum(),
    }
