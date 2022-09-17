import os
from typing import Union

import pandas
from fastapi import FastAPI

app = FastAPI()

scenario_db = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/scenarios")
def list_scenarios():
    load_scenarios()
    print(scenario_db)
    return scenario_db.items()


def load_scenarios():
    global scenario_db
    if len(scenario_db) != 0:
        return
    scenario_files = os.listdir("./data")
    scenario_db = {
        f"Scenario {i}": format_scenario(scenario)
        for i, scenario in enumerate(scenario_files)
    }


def format_scenario(scenario_csv):
    df = pandas.read_csv(f"data/{scenario_csv}", header=None)
    print(df)
    print(df[df[0] == "Electricity|Imports"].squeeze()[1:])
    return {
        "name": f"Scenario {scenario_csv.replace('.csv', '')}",
        "co2": df[df[0] == "CO2|Total"].squeeze().iloc[1],
        "cost": df[df[0] == "Costs|System cost"].squeeze().iloc[1],
        "domestic": df[df[0] == "Electricity|Imports"].squeeze()[1:].sum(),
    }
