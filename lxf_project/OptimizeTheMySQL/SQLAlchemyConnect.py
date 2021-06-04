# 导入:
from sqlalchemy import Column, String, create_engine, Date, DECIMAL, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Project(Base):
    # 表的名字:
    __tablename__ = 'project_column'

    # 表的结构:
    project_id = Column(Integer, primary_key=True)
    inputUserId = Column(Integer)
    subjectCategory = Column(String(20))
    project_code = Column(String(128))
    project_name = Column(String(1024))
    source = Column(String(128))
    datestart = Column(Date)
    type = Column(String(128))
    state = Column(String(128))
    charge = Column(String(128))
    communitycode = Column(String(128))
    funds = Column(String(128))
    auditstatus = Column(String(11))
    auditstatusMessage = Column(String(100))
    creatTime = Column(Date)
    updateTime = Column(Date)
    projecttype = Column(Integer)
    middleCheckStatus = Column(String(11))
    middleCheckStatusMessage = Column(String(128))
    finishStatus = Column(String(11))
    finishStatusMessage = Column(String(128))
    changeStatus = Column(String(11))
    changeStatusMessage = Column(String(128))
    viewCnt = Column(Integer)
    account = Column(DECIMAL(15, 6))
    accountcount = Column(Integer)
    pay = Column(DECIMAL(15, 6))
    paycount = Column(Integer)
    balance = Column(DECIMAL(15, 6))
    isFunds = Column(Integer)
    middleProcessInstanceId = Column(Integer)
    finishProcessInstanceId = Column(Integer)
    fileName = Column(String(100))
    outPay = Column(DECIMAL(15, 6))
    outPayCount = Column(Integer)
    managementFee = Column(DECIMAL(15, 6))


# 定义User对象:
class MetaData(Base):
    # 表的名字:
    __tablename__ = 'project_metadata'

    # 表的结构:
    metadata_value_id = Column(Integer, primary_key=True)
    metadata_field_id = Column(Integer)
    text_value = Column(Text)
    text_lang = Column(String(24))
    place = Column(Integer)
    resource_id = Column(Integer)
    contenttype_id = Column(Integer)
    sys_code = Column(String(24))
    project_page = Column(Integer)


# 初始化数据库连接:
engineSource = create_engine('mysql+mysqlconnector://username:password@host:port/db', echo=True)
# 创建DBSession类型:
DBSessionSource = sessionmaker(bind=engineSource)

# 初始化数据库连接:
engineTarget = create_engine('mysql+mysqlconnector://username:password@host:port/db2', echo=True)
# 创建DBSession类型:
DBSessionTarget = sessionmaker(bind=engineTarget)
