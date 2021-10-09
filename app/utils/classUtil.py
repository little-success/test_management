import os
import re
from requests import Session

get_template = """
import jsonpath as jsonpath
import requests


class {caseName}:

    def setup(self):
        self.url = {api}
        self.params = {}
        
    def test_{caseName}(self):
        res = requests.get(self.url,self.params)
        assert res.status_code == 200
        assert jsonpath.jsonpath(res.json(),'$.code') == [0]

    

"""
post_template = """
import jsonpath as jsonpath
import requests


class {caseName}:

    def setup(self):
        self.url = {api}
        self.json = {}
        
    def test_{caseName}(self):
        res = requests.post(self.url,self.json)
        assert res.status_code == 200
        assert jsonpath.jsonpath(res.json(),'$.code') == [0]



"""

def auto_gen_cases(swagger_url, project_name):
    """
    根据swagger返回的json数据自动生成yml测试用例模板
    :param swagger_url:
    :param project_name:
    :return:
    """
    res = Session().request('get', swagger_url).json()
    data = res.get('paths')

    workspace = os.getcwd()

    project_ = os.path.join(workspace, project_name)

    if not os.path.exists(project_):
        os.mkdir(project_)

    for k, v in data.items():
        pa_res = re.split(r'[/]+', k)
        dir, *case_name = pa_res[1:]

        if case_name:
            case_name = ''.join([x.title() for x in case_name]).casefold()
        else:
            case_name = dir

        file =case_name + '_api.py'

        dirs = os.path.join(project_, dir)

        if not os.path.exists(dirs):
            os.mkdir(dirs)

        os.chdir(dirs)

        if len(v) > 1:
            v = {'post': v.get('post')}
        for _k, _v in v.items():
            method = _k
            api = k
            data_or_params = 'params' if method == 'get' else 'json'
            parameters = _v.get('parameters')
            data_s = ''
            try:
                for each in parameters:
                    data_s += each.get('name')
                    data_s += ': \n'
                    data_s += ' ' * 8
            except TypeError:
                data_s += '{}'

        file_ = os.path.join(dirs, file)

        with open(file_, 'w', encoding='utf-8') as fw:
            fw.write(post_template.format(
                method=method,
                api=api,
                caseName=case_name,
                data_or_params=data_or_params,
                data=data_s
            ))

        os.chdir(project_)

if __name__=='__main__':
    auto_gen_cases('http://www.xiaocheng.tech:8801/v2/api-docs','wexin')

