import re
import os
import sys

from requests import Session

base_url = ""  # 基础地址

get_template = """
teststeps:
-
    name: {caseName}
    variables:

    request:
        method: "{method}"
        url: {url}

        {data}

        headers:
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36
    validate:
        - eq: ["status_code", 200]
"""

post_template = """
teststeps:
-
    name: {caseName}
    variables:

    request:
        method: "{method}"
        url: {url}
        params:
            {params}

        headers:
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36
    validate:
        - eq: ["status_code", 200]
"""


class Auto_get_case:
    data_path = {}
    data_definitions = {}

    def auto_gen_cases(self, swagger_url, project_name):
        """
        根据swagger返回的json数据自动生成yml测试用例模板
        :param swagger_url:
        :param project_name:
        :return:
        """
        res = Session().request('get', swagger_url).json()
        data_path = res.get('paths')  # 获取swagger Json 格式下 paths节点 接口的 path
        definitions = res.get("definitions")  # 获取swagger定义的元数据, param参数

        # 处理swagger元数据
        #
        # for definition, properties in definitions.items():
        #     data_names = {}
        #     for i in properties.get("properties").items():
        #         data_names[f"{i[0]}"] = ""

        workspace = os.getcwd()  # 获取当前文件路径

        project_ = os.path.join(workspace,
                                project_name)  # 获取当前文件目录路径+项目名称，进行拼接 如 C:\Users\Administrator\Desktop\demo\five

        # 创建项目文件
        if not os.path.exists(project_):  # 如果项目文件不存在就创建文件
            os.mkdir(project_)

        # 处理 api路径,进行拼接
        for path_api, path_body in data_path.items():
            pa_res = re.split(r'[/]+', path_api)  # 获取path路径, 切片保存保存为: ['api', 'v1', 'five-elements']
            api, *file = pa_res[1:]
            if file:  # 如果file存在就进行转换
                file = 'test_' + ''.join([x for x in file]).casefold()  # 把 file 首字母转换为大写, 进行拼接
            else:
                file = api

            # 添加文件后缀
            file += '_api.yaml'  # 文件后缀加上 .yml
            dirs = os.path.join(project_, f"test_{api}")  # 使用项目名称+ api 在项目目录下创建 api文件, dir=api,是根据swagger下path返回来的
            if not os.path.exists(dirs):  # 判断项目的 api 是否存在，不存在就创建
                os.mkdir(dirs)

            # 切换工作目录路径
            os.chdir(dirs)  # 方法用于改变当前工作目录到指定的路径

            if len(path_body) > 1:
                path_body = {'post': path_body.get('post')}  # 获取path下 post的 dict信息

            data_s = ''
            params = {}
            # 处理 用例请求方法
            for _k, _v in path_body.items():
                method = _k.upper()  # 获取请求方法
                caseName = f"{_v.get('tags')[0]}-{_v.get('summary')}"  # 获取接口描述
                if method == 'GET':
                    parameters = _v.get('parameters')  # 请求参数内容
                    try:
                        for each in parameters:
                            data_s += each.get('name')
                            data_s += ': \n'
                            data_s += ' ' * 8
                    except TypeError:
                        data_s += '{}'

                    file_ = os.path.join(dirs, file)

                    #  写入get请求用例模板中
                    with open(file_, 'w', encoding='utf-8') as fw:
                        fw.write(get_template.format(
                            # base_url=base_url,
                            method=method,
                            url=base_url + path_api,
                            caseName=caseName,
                            data=data_s,
                        ))
                    os.chdir(project_)

                if method == 'POST':
                    parameters = _v.get('parameters')  # 请求参数内容
                    try:
                        for each in parameters:
                            if each.get("schema"):
                                schema = each.get("schema").get("originalRef")
                                for k_, v_ in definitions.items():
                                    if schema == k_:
                                        for n, m in v_.get("properties").items():
                                            params[f"{n}"] = ''
                    except TypeError:
                        pass

                    file_ = os.path.join(dirs, file)

                    #  写入post请求用例模板中
                    with open(file_, 'w', encoding='utf-8') as fw:
                        fw.write(post_template.format(
                            # base_url=base_url,
                            method=method,
                            url=base_url + path_api,
                            caseName=caseName,
                            params=params,
                        ))

                    os.chdir(project_)


api = 'http://www.xiaocheng.tech:8801/v2/api-docs'  # "swagger 对应服务接口地址"

if __name__ == '__main__':
    a = Auto_get_case()
    a.auto_gen_cases(api, "admin")