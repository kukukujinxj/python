import time
from concurrent.futures.thread import ThreadPoolExecutor

from OptimizeTheMySQL.SQLAlchemyConnect import DBSessionSource, DBSessionTarget, Project


def exe():
    sessionSource = DBSessionSource()
    projectSource = sessionSource.query(Project).limit(300).all()
    sessionSource.close()

    # sessionTarget = DBSessionTarget()
    # projectSource = sessionTarget.query(MetaData).limit(2000).all()
    # sessionTarget.close()

    sessionTarget = DBSessionTarget()
    arr = []
    for item in projectSource:
        project = Project(inputUserId=item.inputUserId, subjectCategory=item.subjectCategory,
                          project_code=item.project_code, project_name=item.project_name, source=item.source,
                          datestart=item.datestart, type=item.type, state=item.state, charge=item.charge,
                          communitycode=item.communitycode, funds=item.funds, auditstatus=item.auditstatus,
                          auditstatusMessage=item.auditstatusMessage, creatTime=item.creatTime,
                          updateTime=item.updateTime, projecttype=item.projecttype,
                          middleCheckStatus=item.middleCheckStatus,
                          middleCheckStatusMessage=item.middleCheckStatusMessage, finishStatus=item.finishStatus,
                          finishStatusMessage=item.finishStatusMessage, changeStatus=item.changeStatus,
                          changeStatusMessage=item.changeStatusMessage, viewCnt=item.viewCnt,
                          middleProcessInstanceId=item.middleProcessInstanceId,
                          finishProcessInstanceId=item.finishProcessInstanceId, fileName=item.fileName,
                          account=item.account, accountcount=item.accountcount, pay=item.pay,
                          paycount=item.paycount,
                          balance=item.balance, isFunds=item.isFunds, outPay=item.outPay,
                          outPayCount=item.outPayCount,
                          managementFee=item.managementFee)
        arr.append(project)
    sessionTarget.add_all(arr)
    sessionTarget.commit()
    sessionTarget.close()


if __name__ == '__main__':
    print('start')
    start = time.time()
    pool = ThreadPoolExecutor(max_workers=5)
    for i in range(10):
        pool.submit(exe)
    pool.shutdown()
    # exe()
    end = time.time()
    print('Task runs %0.2f seconds.' % ((end - start),))
    print('end')
