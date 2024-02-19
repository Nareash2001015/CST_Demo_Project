import json
import subprocess
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('cst', __name__, url_prefix='/cst')


from .file_handle_functions import append_content, append_to_file, prepend_to_file, prepend_content

@bp.post('/')
def filterCST():
    data = json.loads(request.data)
    product_name = data.get("product_name")
    product_base_version = data.get("product_base_version")
    update_level = data.get("update_level")
    project_key = data.get("project_key")
    db = get_db()

    # cst_user = db.execute(
    #         'SELECT customer_name FROM cst_info WHERE product_name = ? and product_base_version = ? and update_level = ? and project_key = ?', 
    #         (product_name, product_base_version, update_level, project_key)
    #     ).fetchall()
    
    # cst_user_list = [row_to_dict(row) for row in cst_user]

    cst_user_list = [
    {
        "customer_name": "WSO2_APIM_HELM_Deployment"
    },
    {
        "customer_name": "MovieReview"
    },
    {
        "customer_name": "Dating_app"
    }
    ]

    prepend_to_file(
        prepend_content(cst_user_list)
    )
    
    append_to_file(
        append_content(cst_user_list)
    )
    
    subprocess.run(['git', 'add', './azure-pipelines.yml'])
    subprocess.run(['git', 'commit', '-m', 'Automated commit: Added CST users'])

    # Push changes to the remote repository (replace origin and branch_name with your actual remote and branch)
    subprocess.run(['git', 'push', 'origin', 'main'])
    
    try:
        response = requests.get('https://dev.azure.com/cs-cst-rnd-001/Web application/_apis/pipelines/9/runs?api-version=7.0')
        response.raise_for_status()
        # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        print(error)
    # This code will run if there is a 404 error.

    return cst_user_list