# coding:utf-8
import requests
import json
import time
import gitlabUtil as git
private_token = '1KpjiCRyt2ywJq3tRwjD'
private_host = 'http://10.100.21.13'
private_date = '2019-01'

def skipProject(pro):
    projects=['skylarkserver','dlock','larknestweb','larknest','larktask']
    if pro.get('name') in projects:
        return False
    else:
        return True
def skipXYProject(pro):
    if str(pro.get('name')).lower().startswith('xy'):
        return True
if __name__ == '__main__':
    sT = time.time()
    projects = git.getAllProjects()
    i = 1
    total = {}
    for pro in projects:
        if pro.get('group') != 'java':
            continue
        if skipProject(pro): #指定工程
            continue
        if skipXYProject(pro): #排除部分xy开头的工程
            continue
        print('start project:::' + pro.get('name')+',index:::'+str(i))
        if private_date != '': #指定统计月份
            activitytime = pro.get('activitytime')
            if activitytime < str(private_date+'-01'): # 不活跃的不统计
                print('skip unactiviry project:::' + pro.get('name'))
                continue
            r = git.coutProjectBydate(pro,private_date)
        else:
            r = git.coutProject(pro)
        rl = git.converStr(r)  #处理结果字符串转义
        print('finish project:::' + json.dumps(rl,encoding='utf-8',ensure_ascii=False))
        git.mcount(total,rl)  #处理结果汇总
        #print('now total is:::' + str(total))
        i += 1
    print('-------total------\n')
    dict = sorted(total.items(), key=lambda d: d[1], reverse=True)  #排序
    git.report(dict) #打印
    eT = time.time()
    exT = eT-sT
    print('Time used:::'+str(int(exT))+'S')
