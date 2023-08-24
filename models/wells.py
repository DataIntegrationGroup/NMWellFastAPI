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
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER as GUID
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Well(Base):
    __tablename__ = "tbl_well_locations"

    OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID)

    API = Column(String(12))

    Lat_dd83 = Column(Float)
    Long_dd83 = Column(Float)

    records = relationship("Records", backref="well")

    @property
    def geometry(self):
        lat, lon = self.Lat_dd83, self.Long_dd83
        # elevation = self.Altitude
        # altitude is in ft above sea level geojson wants meters
        # if elevation is not None:
        #     convert feet to meters
        # elevation *= 0.3048

        return {"coordinates": [lon, lat], "type": "Point"}


class Records(Base):
    __tablename__ = "tbl_well_records"

    RecrdSetID = Column(GUID, primary_key=True, index=True)
    # OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID, ForeignKey("tbl_well_locations.WellDataID"))
    ActionDate = Column(DateTime)
    WellName = Column(String(50))
    WellNumber = Column(String(50))
    API_suffix = Column(String(4))
    # EnteredBy
    # EntryDate
    # Comments


# ============= EOF =============================================
