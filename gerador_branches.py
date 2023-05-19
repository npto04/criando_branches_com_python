import datetime
import subprocess
import yaml
import logging

# Configurações
params_file = "params.yml"
start_date = datetime.datetime.strptime('2019-01-01', r'%Y-%m-%d')
num_years = 12

# Configurações de log
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Funções
def create_git_branch(params_file: str, start_date: datetime.datetime, end_date):
    branch_name = f"params_{start_date.year}"
    logger.info(f"Creating branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name])
    update_params_file(params_file, start_date, end_date)
    logger.info(f"Adding {params_file} to branch {branch_name}")
    subprocess.run(["git", "add", params_file])
    logger.info(f"Commiting {params_file} to branch {branch_name}")
    subprocess.run(["git", "commit", "-m", f"Add {branch_name} version of params.yml"])
    logger.info(f"Pushing {branch_name} to remote")
    subprocess.run(["git", "push", "origin", branch_name])

def update_params_file(params_file: str, start_date: datetime.datetime, end_date: datetime.datetime):
    logger.info(f"Updating {params_file} with {start_date} and {end_date}")
    with open(params_file, 'r') as file:
        params = yaml.safe_load(file)

    params['collect']['data-inicio-treino'] = start_date.strftime(r'%Y-%m-%d')
    params['collect']['data-fim-treino'] = end_date.strftime(r'%Y-%m-%d')

    with open(params_file, 'w') as file:
        yaml.dump(params, file)

def generate_git_branches(params_file: str, start_date: datetime.datetime, num_years: int):
    logger.info(f"Generating {num_years} branches")
    for _ in range(num_years):
        create_git_branch(params_file, start_date, start_date.replace(year=start_date.year-1) - datetime.timedelta(days=1))
        logger.info(f"Branch {start_date.year} created")
        start_date = start_date.replace(year=start_date.year-1)


# Execução
if __name__ == "__main__":
    generate_git_branches(params_file, start_date, num_years)
