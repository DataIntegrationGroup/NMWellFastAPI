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
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import wells
from dependencies import get_db

router = APIRouter(prefix="/api/v1/wells", tags=["wells"])


@router.get("/{well_id}")
def get_well(well_id: int, db: Session = Depends(get_db)):
    return db.query(wells.Well).filter(wells.Well.OBJECTID == well_id).first()


@router.get("/")
def get_wells(f: str = None, db: Session = Depends(get_db)):
    rows = db.query(wells.Well).all()

    def tofeature(w):
        return {
            "type": "Feature",
            "properties": {
                "name": w.OBJECTID,
            },
            "geometry": w.geometry,
        }

    if f == "geojson":
        ret = {"type": "FeatureCollection", "features": [tofeature(w) for w in rows]}
    else:
        ret = rows

    return ret


# ============= EOF =============================================
