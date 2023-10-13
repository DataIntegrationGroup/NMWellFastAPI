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
from datetime import datetime

from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER as GUID
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
    MetaData,
    Table,
    BLOB,
)
from sqlalchemy.orm import relationship, declared_attr

from database import Base, engine


# metadata = MetaData(bind=engine)


class TableMixin:
    @declared_attr
    def __tablename__(self):
        return f"Well_{self.__name__}"


class GlobalIDMixin(TableMixin):
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


class LUMixin:
    @declared_attr
    def __tablename__(self):
        return self.__name__


# class LU_WorkType(Base, LUMixin):
#     Code = Column(String(50), primary_key=True)
#     Value = Column(String(50))
#     Comments = Column(String(50))


class Bore(Base, GlobalIDMixin, RecordSetMixin):
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
    Month_ = Column(Integer)
    Day_ = Column(Integer)
    Year_ = Column(Integer)
    Information = Column(String())
    WorkType = Column(String(24))

    # WorkType = Column(String(24), ForeignKey("LU_WorkType.Code"))
    # work_type_ = relationship("LU_WorkType")
    # @property
    # def worktype_meaning(self):
    #     return self.work_type_.Value


class Header(Base, TableMixin):
    OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID, ForeignKey("Well_Location.WellDataID"))
    API = Column(String(14))


class History(Base, GlobalIDMixin, RecordSetMixin):
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
    Comments = Column(String(255))
    Sax = Column(Integer)
    ToDepth = Column(Float)
    FromDepth = Column(Float)
    LinerSize = Column(Float)


class LithLog(Base, GlobalIDMixin, RecordSetMixin):
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


class Location(Base, TableMixin):
    OBJECTID = Column(Integer, primary_key=True, index=True)
    WellDataID = Column(GUID)

    Lat_dd83 = Column(Float)
    Long_dd83 = Column(Float)

    records = relationship("Records", backref="well")
    spots = relationship("Spots", backref="well")
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


class LogData(Base, GlobalIDMixin, RecordSetMixin):
    LogClass = Column(String(24))
    LogType = Column(String(8))
    LogTitle = Column(String(255))
    LogDate = Column(DateTime)
    FromDepth = Column(Float)
    ToDepth = Column(Float)
    Hotlink = Column(String(255))
    FileNo = Column(Integer)
    FileLoc = Column(String(255))
    Int_Notes = Column(String(255))


class LithStrat(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_LthStrat"

    LithClass = Column(String(50))
    UnitBasis = Column(String(16))
    UnitName = Column(String(128))
    GeoID = Column(String(16))
    WithinUnit = Column(String(16))
    Top_Qual = Column(String(3))
    Depth2Top = Column(Float)
    Top_TVD = Column(Float)
    Elev_Top = Column(Float)
    Botm_Qual = Column(String(3))
    Depth2Botm = Column(Float)
    Bottom_TVD = Column(Float)
    Elev_Bot = Column(Float)
    DpthMethod = Column(String(16))
    PickConfid = Column(String(16))
    Absent = Column(Integer)
    Overturned = Column(Integer)
    Duplicated = Column(Integer)
    Exclude = Column(Integer)
    CheckPick = Column(Integer)
    Int_Notes = Column(String(255))


class PerfIntv(Base, GlobalIDMixin, RecordSetMixin):
    """
    __table__ = Table('Well_PerfIntv', metadata, autoload=True)
    because this views dont have a primary key sqlalchemy will not load them
    ask Mark to add primary keys to the views?
    """

    PerfType = Column(String(8))
    Comments = Column(String(255))
    DepthType = Column(String(5))
    PrfToDpth = Column(Float)
    PrfFrmDpth = Column(Float)
    PrdIntvlID = Column(GUID)


class PetroDat(Base, RecordSetMixin):
    __tablename__ = "Well_PetroDat"
    PrdIntvlID = Column(GUID, primary_key=True, index=True)
    ProdFm = Column(String(128))
    Field_Pool = Column(String(128))
    PrdFrmDpth = Column(Float)
    PrdToDepth = Column(Float)
    Int_Notes = Column(String(255))
    OCD_PoolID = Column(String(10))


class Production(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Productn"
    InitialProd = Column(DateTime())
    Method = Column(String(24))
    ProdQual = Column(String(24))
    ChokeSize = Column(Float)
    ChokeQual = Column(String(24))
    ProdZone = Column(String(50))
    GOR = Column(Float)
    GORqual = Column(String(24))
    FTP = Column(Float)
    FTPmin = Column(Float)
    FTPmax = Column(Float)
    FTPunits = Column(String(4))
    SITP = Column(Float)
    SITPunits = Column(String(4))
    SICP = Column(Float)
    SICPunits = Column(String(4))
    CsgPress = Column(Float)
    CsgPressUn = Column(String(4))
    CsgPrsQual = Column(String(16))
    BOPD = Column(Float)
    BOPDqual = Column(String(8))
    TraceOil = Column(Integer)
    MCFGD = Column(Float)
    MillMCFGD = Column(Float)
    MCFGDqual = Column(String(8))
    BWD = Column(Float)
    BWDqual = Column(String(8))
    APIoilGrav = Column(Float)
    OilGravqu = Column(String(16))
    GasGrav = Column(Float)
    GasGravqu = Column(String(16))
    IP = Column(String(4))
    GasBTU = Column(Float)
    MiscInfo = Column(String)


class Records(Base, TableMixin):
    RecrdSetID = Column(GUID, primary_key=True, index=True)
    OBJECTID = Column(Integer)
    WellDataID = Column(GUID, ForeignKey("Well_Location.WellDataID"))
    ActionDate = Column(DateTime)
    WellName = Column(String(50))
    WellNumber = Column(String(50))
    API_suffix = Column(String(4))
    EnteredBy = Column(String(4))
    EntryDate = Column(DateTime)
    Comments = Column(String(255))

    bore = relationship("Bore", backref="records")
    casing = relationship("Casing", backref="records")
    drillers = relationship("Drillers", backref="records")
    history = relationship("History", backref="records")
    liner = relationship("Liner", backref="records")
    lithlog = relationship("LithLog", backref="records")
    logdata = relationship("LogData", backref="records")
    lithstrat = relationship("LithStrat", backref="records")
    perforation = relationship("PerfIntv", backref="records")
    petro = relationship("PetroDat", backref="records")
    production = relationship("Production", backref="records")
    samples = relationship("Samples", backref="records")
    tubing = relationship("Tubing", backref="records")
    treatments = relationship("Treatment", backref="records")


class Samples(Base, RecordSetMixin):
    __tablename__ = "Well_Samples"
    OBJECTID = Column(Integer)
    SamplSetID = Column(GUID, primary_key=True, index=True)
    SmpSetName = Column(String(128))
    SamplClass = Column(String(24))
    SampleType = Column(String(50))
    SampleFm = Column(String(50))
    SampleLoc = Column(String(128))
    SampleDate = Column(DateTime)
    From_Depth = Column(Float)
    To_Depth = Column(Float)
    SmpDpUnt = Column(String(16))
    From_TVD = Column(Float)
    To_TVD = Column(Float)
    From_Elev = Column(Float)
    To_Elev = Column(Float)
    Porosity = Column(Integer)
    Permeablty = Column(Integer)
    Density = Column(Integer)
    DST_Tests = Column(Integer)
    ThinSect = Column(Integer)
    Geochron = Column(Integer)
    Geochem = Column(Integer)
    Geothermal = Column(Integer)
    WholeRock = Column(Integer)
    Paleontlgy = Column(Integer)
    EnteredBy = Column(String(4))
    EntryDate = Column(DateTime)
    Notes = Column(String(255))

    tempvsdepths = relationship("TempVsDepth", backref="samples")
    intervals = relationship("Intervals", backref="samples")
    bhtheaders = relationship("BHTheaders", backref="samples")


class BHTheaders(Base):
    __tablename__ = "GT_BHTheader"
    BHTGUID = Column(GUID, primary_key=True, index=True)
    SamplSetID = Column(GUID, ForeignKey("Well_Samples.SamplSetID"))
    BoreDia = Column(Float)

    data = relationship("BHTdata", backref="bht")


class BHTdata(Base):
    __tablename__ = "GT_BHTdata"
    BHTGUID = Column(GUID, ForeignKey("GT_BHTheader.BHTGUID"), primary_key=True)
    BHT = Column(Float)
    Depth = Column(Float)


class Intervals(
    Base,
):
    __tablename__ = "WS_Interval"
    IntrvlGUID = Column(GUID, primary_key=True, index=True)
    SamplSetID = Column(GUID, ForeignKey("Well_Samples.SamplSetID"))
    From_Depth = Column(Float)
    To_Depth = Column(Float)

    heatflows = relationship("HeatFlow", backref="intervals")
    conductivities = relationship("ThermalConductivity", backref="intervals")


class ThermalConductivity(Base, GlobalIDMixin):
    __tablename__ = "GT_Conductvty"
    IntrvlGUID = Column(GUID, ForeignKey("WS_Interval.IntrvlGUID"))
    Cnductvity = Column(Float)


class HeatFlow(Base, GlobalIDMixin):
    __tablename__ = "GT_HeatFlow"
    IntrvlGUID = Column(GUID, ForeignKey("WS_Interval.IntrvlGUID"))
    Ka = Column(Float)
    Kpr = Column(Float)


class TempVsDepth(Base, GlobalIDMixin):
    __tablename__ = "GT_TempDepth"
    Depth = Column(Float)
    Temp = Column(Float)
    SamplSetID = Column(GUID, ForeignKey("Well_Samples.SamplSetID"))


class Spots(Base, TableMixin):
    DsplyScale = Column(Integer)
    Import_ID = Column(Integer)
    FGDC_code = Column(String(16))
    Well_ID = Column(String(50))
    WellDataID = Column(GUID, ForeignKey("Well_Location.WellDataID"))
    WellSpotID = Column(GUID, primary_key=True, index=True)
    SHAPE = Column(BLOB)
    OBJECTID = Column(Integer)


class Treatment(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Treatmnt"
    Comments = Column(String(255))
    Treatment = Column(String())
    ToDepth = Column(Float)
    FromDepth = Column(Float)


class Tubing(Base, GlobalIDMixin, RecordSetMixin):
    __tablename__ = "Well_Tubing"
    Comments = Column(String(255))
    PackerSet = Column(Integer)
    TubingDepth = Column(Float)
    TubingSize = Column(Float)


# ============= EOF =============================================
