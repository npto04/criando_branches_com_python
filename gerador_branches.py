import datetime
import subprocess

def create_git_branch(params_file, start_date, end_date):
    branch_name = f"params_{start_date.year}"
    subprocess.run(["git", "checkout", "-b", branch_name])
    subprocess.run(["cp", params_file, "params.yml"])
    subprocess.run(["git", "add", "params.yml"])
    subprocess.run(["git", "commit", "-m", f"Add {branch_name} version of params.yml"])
    subprocess.run(["git", "push", "origin", branch_name])

def generate_git_branches(params_file, start_date, end_date):
    current_date = start_date
    while current_date.year <= end_date.year:
        create_git_branch(params_file, current_date, current_date.replace(year=current_date.year+1) - datetime.timedelta(days=1))
        current_date = current_date.replace(year=current_date.year+1)

# Configurações
params_file = "params.yml"
start_date = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2019-12-31', '%Y-%m-%d')

generate_git_branches(params_file, start_date, end_date)
