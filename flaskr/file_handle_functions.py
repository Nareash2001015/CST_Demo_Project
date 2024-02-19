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