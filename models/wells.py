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
from sqlalchemy.orm import relationship, declared_attr

from database import Base


class GlobalIDMixin:
    @declared_attr
    def GlobalID(self):
        return Column(GUID, primary_key=True, index=True)

    @declared_attr
    def OBJECTID(self):
        return Column(Integer)


class RecordSetMixin:
    @declared_attr
    def RecrdsetID(self):
        return Column(GUID, ForeignKey("Well_Records.RecrdSetID"))


class Bore(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Bore"

    FromDepth = Column(Float)
    ToDepth = Column(Float)
    DrillMethd = Column(String(50))
    BoreDia = Column(Float)
    BoreUnits = Column(String(16))
    DrillFluid = Column(String(16))
    FldSalinity = Column(Float)
    FldRstvity = Column(Float)
    Fluid_pH = Column(Float)
    FldDensity = Column(Float)
    FldLevel = Column(Float)
    FldViscsty = Column(Float)
    FluidLoss = Column(String(50))
    Comments = Column(String(255))


class Casing(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Casing"

    Depth = Column(Float)
    CasingType = Column(String(50))
    CasDiaType = Column(String(2))
    CasingMtrl = Column(String(50))
    CasingDiam = Column(Float)
    CasDiaUnit = Column(String(16))
    CasDpthDrl = Column(Float)
    CasDpthLog = Column(Float)
    CasingWgt = Column(Float)
    CasngWgtUn = Column(String(8))
    CasngThick = Column(Float)
    CasngThkUn = Column(String(16))
    CasingLen = Column(Float)
    CasLenUnit = Column(String(16))
    Sax = Column(Integer)
    CmntRcd = Column(String(25))
    Comments = Column(String(255))
    DepthType = Column(String(8))


class Drillers(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Drillers"

    Month_ = Column(Integer)
    Day_ = Column(Integer)
    Year_ = Column(Integer)
    WorkType = Column(String(24))
    Information = Column(String())


class History(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_History"
    ActionClss = Column(String(16))
    WorkType = Column(String(16))
    ActionDate = Column(DateTime)
    SpudDate = Column(DateTime)
    Commodity = Column(String(16))
    PlugBack = Column(Float)
    BridgePlug = Column(String(50))
    TotalDepth = Column(Float)
    Results = Column(String(16))
    LeaseID = Column(String(128))
    Operator = Column(String(50))
    Contractor = Column(String(50))
    Driller = Column(String(50))
    Status = Column(String(16))


class Liner(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Liner"
    Comments = Column(String(255))
    Sax = Column(Integer)
    ToDepth = Column(Float)
    FromDepth = Column(Float)
    LinerSize = Column(Float)


class LithLog(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_LithLog"
    GeoID = Column(String(16))
    FromDepth = Column(Float)
    Name = Column(String(128))
    ToDepth = Column(Float)
    LithClass = Column(String(50))
    LithType = Column(String(50))
    IgneousCmp = Column(String(50))
    MMfacies = Column(String(50))
    Mineralogy = Column(String(255))
    PrimLith = Column(String(128))
    SecondLith = Column(String(128))
    ShortDesc = Column(String(255))
    UnitDesc = Column(String())
    Texture = Column(String(255))
    Color = Column(String(255))
    GrainSize = Column(String(255))
    Sorting = Column(String(255))
    Cemntation = Column(String(255))
    Induration = Column(String(255))
    Bedding = Column(String(255))
    BedThkness = Column(Float)
    ThickUnits = Column(String(8))
    Protolith = Column(String(255))
    Comments = Column(String(255))


class Location(Base):
    __tablename__ = "Well_Location"

    OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID)

    Lat_dd83 = Column(Float)
    Long_dd83 = Column(Float)

    records = relationship("Records", backref="well")
    header = relationship("Header", backref="well", uselist=False)

    @property
    def geometry(self):
        lat, lon = self.Lat_dd83, self.Long_dd83
        # elevation = self.Altitude
        # altitude is in ft above sea level geojson wants meters
        # if elevation is not None:
        #     convert feet to meters
        # elevation *= 0.3048

        return {"coordinates": [lon, lat], "type": "Point"}


class Header(Base):
    __tablename__ = "Well_Header"

    OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID, ForeignKey("Well_Location.WellDataID"))
    API = Column(String(14))


class Records(Base):
    __tablename__ = "Well_Records"

    RecrdSetID = Column(GUID, primary_key=True, index=True)
    OBJECTID = Column(Integer)
    WellDataID = Column(GUID, ForeignKey("Well_Location.WellDataID"))
    ActionDate = Column(DateTime)
    WellName = Column(String(50))
    WellNumber = Column(String(50))
    API_suffix = Column(String(4))
    # EnteredBy
    # EntryDate
    # Comments

    bore = relationship("Bore", backref="records")
    casing = relationship("Casing", backref="records")
    drillers = relationship("Drillers", backref="records")
    history = relationship("History", backref="records")
    liner = relationship("Liner", backref="records")
    lithlog = relationship("LithLog", backref="records")


# ============= EOF =============================================
