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
from sqlalchemy import text
from sqlalchemy.orm import Session

from models import wells
from dependencies import get_db

router = APIRouter(prefix="/api/v1/wells", tags=["wells"])


@router.get("/")
def get_wells(f: str = None, db: Session = Depends(get_db)):
    # rows = db.query(wells.Well).filter(wells.Well.API.is_not(None)).limit(10).all()
    rows = db.query(wells.Location, wells.Header).join(wells.Header).all()

    # rows = db.query(wells.Well).all()

    def tofeature(w, h):
        return {
            "type": "Feature",
            "properties": {
                "name": w.OBJECTID,
                "well_id": w.OBJECTID,
                "api": h.API,
            },
            "geometry": w.geometry,
        }

    if f == "geojson":
        ret = {"type": "FeatureCollection", "features": [tofeature(*w) for w in rows]}
    else:
        ret = rows

    return ret


def get_well_db(well_id, db):
    well = db.query(wells.Location).filter(wells.Location.OBJECTID == well_id).first()
    return well


def get_recordset_assoc(attr, well_id, db):
    well = get_well_db(well_id, db)
    return [getattr(r, attr) for r in well.records]


@router.get("/{well_id}")
def get_well(well_id: int, db: Session = Depends(get_db)):
    well = get_well_db(well_id, db)
    return well


@router.get("/{well_id}/records")
def get_well_records(well_id: int, db: Session = Depends(get_db)):
    well = get_well_db(well_id, db)
    return well.records


@router.get("/{well_id}/bore")
def get_well_bore(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("bore", well_id, db)


@router.get("/{well_id}/casing")
def get_well_casing(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("casing", well_id, db)


@router.get("/{well_id}/drillers")
def get_well_drillers(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("drillers", well_id, db)


@router.get("/{well_id}/header")
def get_well_header(well_id: int, db: Session = Depends(get_db)):
    well = get_well_db(well_id, db)
    return well.header


@router.get("/{well_id}/history")
def get_well_history(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("history", well_id, db)


@router.get("/{well_id}/liner")
def get_well_liner(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("liner", well_id, db)


@router.get("/{well_id}/lithlog")
def get_well_lithlog(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("lithlog", well_id, db)


@router.get("/{well_id}/lithstrat")
def get_well_lithstrat(well_id: int, db: Session = Depends(get_db)):
    return get_recordset_assoc("lithstrat", well_id, db)


# ============= EOF =============================================
