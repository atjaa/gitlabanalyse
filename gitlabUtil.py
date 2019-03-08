# coding:utf-8
import requests
import os
import json
private_token = '1KpjiCRyt2ywJq3tRwjD'
private_host = 'http://10.100.21.13'
def get100Projects(page):
    r = requests.get(private_host + '/api/v3/projects?private_token=' + private_token + '&per_page=100'+'&page='+str(page))
    data = r.json()
    projects = []
    for i in data:
        project = {}
        project['id'] = i['id']
        project['name']=i['name']
        project['url']=i['http_url_to_repo']
        project['group']=str(i['path_with_namespace']).split('/')[0]
        project['activitytime']=str(i['last_activity_at']).split('T')[0]
        projects.append(project)
    return projects
def getAllProjects():
    page = 1
    projects = []
    donext = True
    while donext:
        pros = get100Projects(page)
        for pro in pros:
            projects.append(pro)
        page=page+1
        if len(pros) < 100:
            donext = False
    return projects
def coutProject(project):
    commands = 'git log --format=\'%cN\' | sort -u | while read name; do echo -en \"$name*\"; git log --author=\"$name\" --pretty=tformat: --numstat | awk \'{ add += $1; subs += $2; loc += $1 - $2 } END { printf \"%s*%s*%s@\", add, subs, loc }\' -; done'
    out = os.popen('git clone '+project.get('url')+'&& cd '+project.get('name')
                   +'&&'+commands+'&& cd .. && rm -rf '+project.get('name'))
    return out.read()
def coutProjectBydate(project,date):
    commands = 'git log --format=\'%cN\' | sort -u | while read name; do echo -en \"$name*\"; git log --author=\"$name\" --since='+date+'-01 --until='+date+'-31 --pretty=tformat: --numstat | awk \'{ add += $1; subs += $2; loc += $1 - $2 } END { printf \"%s*%s*%s@\", add, subs, loc }\' -; done'
    out = os.popen('git clone ' + project.get('url') + '&& cd ' + project.get('name')
                   + '&&' + commands + '&& cd .. && rm -rf ' + project.get('name'))
    return out.read()
def converStr(out):
    out = out.replace('\n', '')
    l = out.split('@')
    l = [item for item in filter(lambda x: x != '', l)]
    rl = []
    for s in l:
        try:
            ul=s.split('*')
            rs={}
            rs['name'] = ul[0]
            v1=ul[1] if ul[1] != '' else 0
            v2=ul[2] if ul[2] != '' else 0
            v3=ul[3] if ul[3] != '' else 0
            rs['added'] = int(v1)
            rs['removed'] = int(v2)
            rs['total'] = int(v3)
            rl.append(rs)
        except Exception,e:
            print('convertStr err:::'+str(e))
    return rl
def mcount(total,rl):
    for per in rl:
        if total.get(per.get('name')):
            p = total.get(per.get('name'))
            p['added'] += int(per.get('added'))
            p['removed'] += int(per.get('removed'))
            p['total'] += int(per.get('total'))
        else:
            total[per.get('name')]=per
def report(total):
    for name in total:
        #if int(total.get(name).get('added'))==0 and int(total.get(name).get('removed'))==0 and int(total.get(name).get('total'))==0:
        #    continue
        if int(name[1].get('added'))==0 and int(name[1].get('removed'))==0 and int(name[1].get('total'))==0:
            continue
        print(json.dumps(name[0],encoding='utf-8',ensure_ascii=False).replace('-en ','').replace('\"','')
              +'\t'+json.dumps(name[1],encoding='utf-8',ensure_ascii=False).replace('-en ','').replace(' ','').replace('{','').replace('}','').replace(',','\t').replace('\'','').replace('\"',''))