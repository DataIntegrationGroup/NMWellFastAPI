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
import os
from pathlib import Path

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app import app

from routes import wells

app.include_router(wells.router)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@app.get("/mapboxtoken")
def mapboxtoken():
    return {
        "token": os.environ.get('MAPBOX_TOKEN')
    }


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
