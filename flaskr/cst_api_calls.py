import time
import json
import requests
import subprocess
from .file_handle_functions import append_content, append_to_file, prepend_to_file, prepend_content, row_to_dict, get_build_response, get_build_timeline_response
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('cst', __name__, url_prefix='/cst')

#### API call to filter cst customers

@bp.post('/')
def filterCST():
    data = json.loads(request.data)
    product_name = data.get("product_name")
    product_base_version = data.get("product_base_version")
    update_level = data.get("update_level")
    project_key = data.get("project_key")
    db = get_db()

    cst_user = db.execute(
            'SELECT customer_key, product_name, product_base_version FROM cst_info WHERE product_name = ? and product_base_version = ? and update_level = ? and project_key = ?', 
            (product_name, product_base_version, update_level, project_key)
        ).fetchall()
    
    cst_user_list = [row_to_dict(row) for row in cst_user]

    return cst_user_list

#### API call to trigger the pipeline

@bp.post('/trigger')
def trigger_pipeline():
    
    data = request.json

    # repo_names = objects_to_strings(data)
    
    repo_names = [
    {
        "customer_key": "WSO2_APIM_HELM_Deployment"
    },
    {
        "customer_key": "MovieReview"
    },
    {
        "customer_key": "Dating_app"
    }
    ]
    
    prepend_to_file(
        prepend_content(repo_names)
    )
    
    append_to_file(
        append_content(repo_names)
    )
    
    subprocess.run(['git', 'add', './azure-pipelines.yml'])
    subprocess.run(['git', 'commit', '-m', 'Automated commit: Added CST users'])

    subprocess.run(['git', 'push', 'origin', 'main'])
    time.sleep(10)
    
    return get_build_response()

### API call to get the job status

@bp.get('/build')
def get_jobs():
    build_id = request.args.get('build_name')
    timeline_url = get_build_timeline_response(build_id)
    
    response = requests.get(timeline_url)
    
    job_records = response.json()["records"]
    
    filtered_objects = [obj for obj in job_records if obj["identifier"] is not None and obj["identifier"].endswith("__default")]\
    
    extract_fields = []
    
    for obj in filtered_objects:
        if(obj['state'] == "inProgress" or obj['state'] == "pending"):
            print("true")
            extract_fields.append({
                "name": obj["name"].split()[-1],
                "state": obj['state'],
                "result": obj['result'],
            })
        else:
            extract_fields.append({
                "name": obj["name"].split()[-1],
                "state": obj['state'],
                "result": obj['result'],
                "message": obj["log"]["url"]
            })
    
    return extract_fields
    
    