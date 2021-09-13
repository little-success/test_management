import os
import re

import requests

get_template = """
import jsonpath as jsonpath
import requests


class {caseName}:

    def setup(self):
        self.url = 'base_url+{url}'
        self.params = {data}

    def test_{case_name}(self):
        res = requests.get(self.url,self.params)
        assert res.status_code == 200
        assert jsonpath.jsonpath(res.json(),'$.code') == [0]


"""
post_template = """
import jsonpath as jsonpath
import requests


class {caseName}:

    def setup(self):
        self.url = 'base_url+{url}'
        self.json = {data}

    def test_{case_name}(self):
        res = requests.post(self.url,json=self.json)
        assert res.status_code == 200
        assert jsonpath.jsonpath(res.json(),'$.code') == [0]


"""
def create_case(swagger_url, project_name):
    res = requests.get(swagger_url).json()
    paths = res.get('paths')
    workspace = os.getcwd()
    project_ = os.path.join(workspace, project_name)

    if not os.path.exists(project_):
        os.mkdir(project_)
    for k,v in paths.items():
        url = k
        names = re.split(r'[/]+', k)
        case_name = names[-1]
        params = ''
        caseName = 'Test'+ case_name.capitalize() + 'Api'
        file_name = 'test_' + case_name.casefold() +'_api.py'

        for method,v1 in v.items():
                parameters = v1.get('parameters')
                if method == 'get':
                    try:
                        for each in parameters:
                            params += each.get('name')
                            params += ': \n'
                    except TypeError:
                        params += '{}'
                    file_ = os.path.join(project_, file_name)
                    with open(file_, 'w', encoding='utf-8') as fw:
                        fw.write(get_template.format(
                            url=url,
                            case_name=case_name,
                            data=params,
                            caseName=caseName
                        ))

                else:
                    try:
                        for each in parameters:
                            if each.get("schema"):
                                schema = each.get("schema").get("originalRef")
                                if schema is not None:
                                    for k_, v_ in res.get("definitions").items():
                                        if schema == k_:
                                            for n, m in v_.get("properties").items():
                                                params += n
                                                params += ': \n'
                                else:
                                    params += '{}'
                    except TypeError:
                        params += '{}'
                    file_ = os.path.join(project_, file_name)

                    with open(file_, 'w', encoding='utf-8') as fw:
                        fw.write(post_template.format(
                            url=url,
                            case_name=case_name,
                            data=params,
                            caseName=caseName
                        ))
                    

create_case('https://testswca.kakahui.net//v3/api-docs','admin')







def get_base_name(json_data, index=None):
    tags = json_data.get('tags')
    description = []
    for i in range(len(tags)):
        description.append(tags[i].get('description').casefold())
    if index is None:
        return description
    else:
        return description[index]


def get_real_name(base_name,type='.yaml'):
    dirs = ''
    dir = ''
    pa_res = re.split(' ', base_name)
    file = pa_res
    print(pa_res)
    for i in range(len(file)):
        dir += file[i]+'_'
    dir += dir+type
    dirs = os.path.join('admin',dir)
    return dirs


#
# print(get_base_name(res))
# print(get_real_name('app switch controller'))


# def get_case_name():
#     case_name =[]
#     for k, v in data.items():
#         pa_res = re.split(r'[/]+', k)
#         dir = pa_res[-1]
#         case_name.append(''.join([x.casefold() for x in dir]))
#     return case_name

#
# file = 'test_' + ''.join([x for x in 'file']).casefold()
# dirs = os.path.join('project_', f"test_{file}")
#
# if len(path_body) > 1:
#     path_body = {'post': path_body.get('post')}
#
# print(file)