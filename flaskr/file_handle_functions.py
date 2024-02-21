import requests
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

# Personal access token
token = os.getenv('pat')
organization_name = os.getenv('ORGANIZATION_NAME')
project_name = os.getenv('PROJECT_NAME')
pipeline_id = os.getenv('PIPELINE_ID')

filename = "/home/nareash/Desktop/master_repo/azure-pipelines.yml"

### Function to convert returned row from databse to a list

def row_to_dict(row):
    return{
        "customer_key" : row[0],
        "product_name" : row[1],
        "product_version" : row[2]
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
        
#### Function to remove the previous jobs from the azure-pipeline.yml
        
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

    remove_previous_repos()

    content = """resources:
  repositories:
    """
    
    for repo in repo_list:
        content += f"""
  - repository: {repo['customer_key']}
    type: github
    endpoint: github.com_Nareash20010150
    name: Nareash20010150/{repo['customer_key']}
"""
        
    return content


#### Function to prepend the new resources to the azure-pipeline.yml

def append_content(repo_list):

    remove_previous_jobs()
    
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
        content += yaml_template.replace("${{repo_name}}", repo['customer_key'])
        content += "\n"
        
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
    
### returning a list of strings where each string is created by joining customer_key, product_name and product_version
        
def objects_to_strings(object_list):
    string_list = []
    for obj in object_list:
        # Assuming each object has a 'name' attribute
        string_list.append(f"{obj['customer_key']}_{obj['product_name']}_{obj['product_version']}")
    return string_list

### Extract the important fields from the build response and return it  

def get_build_response():
    try:
        req_headers = {'Basic' : f'Basic {token}'}
        req_params = {"api-version" : 7.0}
        response = requests.get(
            f'https://dev.azure.com/{organization_name}/{project_name}/_apis/pipelines/{pipeline_id}/runs',
            headers = req_headers,
            params = req_params,
            json = {'templateParameters': {}})
        build_json = response.json()
        if('result' in build_json["value"][0]):
            build = {
            "build_id" : build_json["value"][0]["name"],
            "result" : build_json["value"][0]["result"],
            "state" : build_json["value"][0]["state"]}
        else:
            build = {
            "build_id" : build_json["value"][0]["name"],
            "state" : build_json["value"][0]["state"]}
            
        return build
    except requests.exceptions.HTTPError as error:
        print(f"Error in getting the builds: {error}")
        
#### 
        
def get_build_timeline_response(build_id):
    try:
        req_params = {"api-version" : 7.0}
        response = requests.get(
            f'https://dev.azure.com/{organization_name}/{project_name}/_apis/build/builds/#{build_id}/timeline/',
            params = req_params)
        build_json = response.json()
        timeline_url = build_json["value"][0]["_links"]["timeline"]["href"]
        return timeline_url
    except requests.exceptions.HTTPError as error:
        print(f"Error in getting the timeline reponse of build id {build_id}: {error}")