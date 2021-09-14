import os
from pathlib import Path

from flask import request
from werkzeug.utils import secure_filename

from run import app


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

    @classmethod
    def api_upload(cls):
        if request.method == 'POST':
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return 'file uploaded successfully'

if __name__ == '__main__':
    FileUtil.api_upload()
