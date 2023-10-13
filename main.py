# ===============================================================================
# Copyright 2023 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import json
import os
from pathlib import Path

import plotly
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app import app
from dependencies import get_db

from routes import wells, injection
from routes.wells import get_well_db

app.include_router(wells.router)
app.include_router(injection.router)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

import plotly.graph_objects as go


def dump_figure(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_intervals(well):
    for ri in well.records:
        print('record', ri, ri.RecrdSetID)
        for si in ri.samples:
            print('sample', si, si.SamplSetID)
            return si.intervals
            # for interval in si.intervals:
            #     print(interval, interval.From_Depth, interval.To_Depth,
            #           interval.heatflows, interval.conductivities,)


def get_bht(well):
    for ri in well.records:
        for si in ri.samples:
            for bht in si.bhtheaders:

                d =  {'diam': bht.BoreDia,
                      'bht': '',
                      'depth': ''}
                if bht.data:
                    d['bht'] = bht.data[0].BHT
                    d['depth'] = bht.data[0].Depth

                return d
    else:
        return {'bht': '', 'diam': '', 'depth': ''}


def get_heatflows(intervals):
    ds = []
    for i in intervals:
        if i.heatflows:
            ds.append((i.From_Depth, i.heatflows[0].Ka))
            # depths.append(i.From_Depth)
            # t.append(i.heatflows[0].Htflow)
    if ds:
        return zip(*sorted(ds, key=lambda x: x[0]))
    else:
        return [], []


def get_thermal_conductivity(intervals):
    ds = []
    for i in intervals:
        if i.conductivities:
            ds.append((i.From_Depth, i.conductivities[0].Cnductvity))
    if ds:
        return zip(*sorted(ds, key=lambda x: x[0]))
    else:
        return [], []


def get_tempvsdepth(well):
    ds = []
    for ri in well.records:
        for si in ri.samples:
            ds.extend([(td.Depth, td.Temp) for td in si.tempvsdepths])

            break
    if ds:
        ds = sorted(ds, key=lambda x: x[0])
        return zip(*ds)
    else:
        return [], []


@app.get("/well/detail/{well_id}", response_class=HTMLResponse)
def well_detail(request: Request, well_id: int, db: Session = Depends(get_db)):
    fig = go.Figure()
    well = get_well_db(well_id, db)
    y, x = get_tempvsdepth(well)

    trace = go.Scatter(x=x, y=y, mode='lines')
    fig.add_trace(trace)
    fig.update_layout(
        margin={"l": 20, "r": 10, "t": 35, "b": 10},
        xaxis={"title": "Temperature (F)"},
        yaxis={"title": "Elevation", "autorange": "reversed"},
    )

    tc_fig = go.Figure()
    hf_fig = go.Figure()
    tc_fig.update_layout(
        margin={"l": 20, "r": 10, "t": 35, "b": 10},
        xaxis={"title": "Thermal Conductivity"},
        yaxis={"title": "Elevation", "autorange": "reversed"},
    )
    hf_fig.update_layout(
        margin={"l": 20, "r": 10, "t": 35, "b": 10},
        xaxis={"title": "Heatflow"},
        yaxis={"title": "Elevation", "autorange": "reversed"},
    )
    intervals = get_intervals(well)
    if intervals:
        depths, t = get_thermal_conductivity(intervals)
        trace = go.Scatter(x=t, y=depths, mode='lines')
        tc_fig.add_trace(trace)

        depths, hs = get_heatflows(intervals)
        trace = go.Scatter(x=hs, y=depths, mode='lines')
        hf_fig.add_trace(trace)


    bht = get_bht(well)
    print('asdf', bht)
    return templates.TemplateResponse(
        "well_detail_view.html",
        {
            "request": request,
            "well_id": well_id,
            'tempvsdepth': dump_figure(fig),
            "thermalconductivity": dump_figure(tc_fig),
            "api": well.header.API or '',
            "bht": bht,
            "heatflow": dump_figure(hf_fig),

            # "center": {"lat": 34.5, "lon": -106.0},
            # "zoom": 7,
            # "data_url": "/locations/fc",
        },
    )


@app.get("/mapboxtoken")
def mapboxtoken():
    return {"token": os.environ.get("MAPBOX_TOKEN")}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "map_view.html",
        {
            "request": request,
            # "center": {"lat": 34.5, "lon": -106.0},
            # "zoom": 7,
            # "data_url": "/locations/fc",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8009)
# ============= EOF =============================================
