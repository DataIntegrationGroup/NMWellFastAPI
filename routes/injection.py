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

from dependencies import get_db

router = APIRouter(prefix="/api/v1/injection", tags=["injection"])


@router.get("/{api_id}")
def get_injection(api_id, db: Session = Depends(get_db)):
    stmt = '''select wellType, wellname, wellstatus, wellcounty from tbl_OCD_WellInjections_InjPressuresByDatePeriod_Life
            where API_WellID_nodash=:api_id'''
    results = db.execute(statement=stmt, params=dict(api_id=api_id))
    # print(results)
    r = results.fetchall()
    # for ri in r:
    #     print(ri)

    return [dict(r) for r in r]


# ============= EOF =============================================
