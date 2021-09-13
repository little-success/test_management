import os
from pathlib import Path


class FileUtil:
    @classmethod
    def create_content(cls, project_name, path=None):
        if path is None:
            workspace = Path.cwd().parent
        else:
            workspace = str(Path.cwd().parent) + path
        project_path = os.path.join(workspace, project_name)
        if not os.path.exists(project_path):
            os.mkdir(project_path)

    @classmethod
    def create_class_file(cls, project_name, path=None):
        if path is None:
            workspace = Path.cwd().parent
        else:
            workspace = str(Path.cwd().parent) + path
        project_path = os.path.join(workspace, project_name)
        if not os.path.exists(project_path):
            os.mkdir(project_path)





if __name__ == '__main__':
    FileUtil.create_content('admin', '/api')
