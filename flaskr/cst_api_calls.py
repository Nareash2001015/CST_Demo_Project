import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('cst', __name__, url_prefix='/cst')

filename = "/home/nareash/Desktop/master_repo/azure-pipelines.yml"

### Function to convert returned row from databse to a list

def row_to_dict(row):
    return{
        "customer_name":row[0]
    }

#### Function to remove the previous resources from the azure-pipeline.yml

def remove_previous_repos():
    with open(filename, 'r+') as f:
        lines = f.readlines()

        # Find the index of the line containing 'trigger:'
        trigger_index = lines.index('trigger:\n')

        # Move the file pointer to the beginning
        f.seek(0)

        # Write the lines from trigger_index onwards back to the file
        f.writelines(lines[trigger_index:])
        
        # Truncate the remaining content (if any)
        f.truncate()
        
def remove_previous_jobs():
    # Read the YAML file
    with open("azure-pipelines.yml", "r") as file:
        yaml_content = file.read()

    # Find the index of the start of the jobs section
    start_index = yaml_content.find("jobs:")

    # Remove all content after the start of the jobs section
    modified_yaml_content = yaml_content[:start_index]

    # Write the modified YAML content back to the file
    with open("azure-pipelines.yml", "w") as file:
        file.write(modified_yaml_content)
    

#### Function to prepend the new resources to the azure-pipeline.yml

def prepend_content(repo_list):

    remove_previous_repos();

    content = """resources:
  repositories:
    """
    
    for repo in repo_list:
        content += f"""
  - repository: {repo['customer_name']}
    type: github
    endpoint: github.com_Nareash20010150
    name: Nareash20010150/{repo['customer_name']}
"""
        
    return content


#### Function to prepend the new resources to the azure-pipeline.yml

def append_content(repo_list):

    remove_previous_jobs();
    
    content = """
  jobs:""" 

    yaml_template = """
  - job: CheckoutAndPrintReadme_${{repo_name}}
    displayName: "Checkout and Print README ${{repo_name}}"
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - checkout: ${{repo_name}}
    - script: |
        echo "Checking out repository: ${{repo_name}}"
        echo "Printing README file for repository: ${{repo_name}}"
        cat README.md
        echo '----------------------------------------------'
"""

    for repo in repo_list:
        content += yaml_template.replace("${{repo_name}}", repo['customer_name'])
        content += "\n"
        
    print(content)
    
    return content
        
### prepending the contents to the begining of the azure-pipeline.yml

def prepend_to_file(content):
    with open(filename, 'r+') as file:
        prev_content = file.read()
        file.seek(0)
        file.write(content + prev_content)
    
### appending the contents to the end of the azure-pipeline.yml

def append_to_file(content):
    with open(filename, "a") as f:
        f.write(content)

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

    return cst_user_list


