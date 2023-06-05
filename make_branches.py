import datetime
import subprocess
import yaml
import logging
from pathlib import Path

# Configurações
## Verifique se o arquivo params.yaml está na mesma pasta que este script e se os parametros abaixo estão corretos
params_file = "params.yaml"
num_years = 12

def get_date(date_param: str) -> datetime.datetime:
    # Load the params file
    with open(Path(params_file).resolve(), "r") as file:
        params = yaml.safe_load(file)

    # Get the start date
    date = datetime.datetime.strptime(params["collect"][date_param], r"%Y-%m-%d")
    return date

# Configurações de log
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Funções
def create_git_branch(params_file: str, start_date: datetime.datetime, end_date: datetime.datetime):
    """
    Creates a git branch for a given params file and date range.

    Args:
        params_file: The name of the params file.
        start_date: The start date of the date range.
        end_date: The end date of the date range.
    """


    branch_name = f"multirrotulo-train-{start_date.year}"

    # Checkout a new branch
    logger.info(f"Creating branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name])

    # Update the params file
    update_params_file(params_file, start_date, end_date)

    logger.info(f"Adding {params_file} to branch {branch_name}")
    subprocess.run(["git", "add", params_file])

    logger.info(f"Commiting {params_file} to branch {branch_name}")
    subprocess.run(["git", "commit", "-m", f"Add {branch_name} version of params.yml"])

    logger.info(f"Pushing {branch_name} to directory")
    # logger.info(f"Pushing {branch_name} to remote")
    # subprocess.run(["git", "push", "origin", branch_name])
    destination_repo = f"/home/modelsbi/data/triagem/{branch_name}"
    logger.info(f"Cloning {branch_name} to {destination_repo}")
    subprocess.run(["git", "clone", ".", destination_repo])
    logger.info(f"Branch {branch_name} created in {destination_repo}")


def update_params_file(
    params_file: str, start_date: datetime.datetime, end_date: datetime.datetime
):
    """
    Update the specified params file with the given start and end dates.

    Args:
        params_file (str): The path to the params file.
        start_date (datetime.datetime): The start date.
        end_date (datetime.datetime): The end date.
    """
    logger.info(f"Updating {params_file} with {start_date} and {end_date}")

    # Check if the params file exists
    params_path = Path(params_file).resolve()
    if params_path.is_file():
        logger.info(f"{params_file} found")
    else:
        logger.error(f"{params_path} not found")
        raise FileNotFoundError(f"{params_file} not found")

    # Load the params file
    with open(Path(params_file).resolve(), "r") as file:
        params = yaml.safe_load(file)

    # Update the date params file
    params["collect"]["data-inicio-treino"] = start_date.strftime(r"%Y-%m-%d")
    params["collect"]["data-fim-treino"] = end_date.strftime(r"%Y-%m-%d")

    # Save the updated params file
    with open(Path(params_file).resolve(), "w") as file:
        yaml.dump(params, file)
    logger.info(f"{params_file} updated")


def generate_git_branches(
    params_file: str, num_years: int
) -> None:
    """
    Create a branch for each year between the start date and the start date minus the number of years.
    Each branch will have a name corresponding to the year.

    Args:
        params_file (str): The name of the params file.
        start_date (datetime.datetime): The start date for the first branch.
        num_years (int): The number of branches to create.
    """

    logger.info(f"Generating {num_years} branches")

    # Get the name of the current branch
    main_branch = (
        subprocess.run(["git", "branch", "--show-current"], capture_output=True)
        .stdout.decode("utf-8")
        .strip()
    )

    # Get the start date for the current iteration
    start_date = get_date("data-inicio-treino")
    logger.info(f"Getting start date for branch {start_date.year}")

    # Get the end date for the current iteration
    end_date = get_date("data-fim-treino")
    logger.info(f"Getting end date for branch {end_date.year}")

    for _ in range(num_years):
        # Checkout main branch
        subprocess.run(["git", "checkout", main_branch])

        # Create a branch for the current year
        create_git_branch(
            params_file,
            start_date,
            end_date,
        )

        logger.info(f"Branch {start_date.year} created")

        # Update the date for the next iteration
        start_date = start_date.replace(year=start_date.year - 1)
        end_date = end_date.replace(year=end_date.year - 1)



# Execução
# params_file is the name of the file with the parameters of the simulation
# start_date is the date of the first commit
# num_years is the number of years to simulate
if __name__ == "__main__":
    logger.info("Workdir: %s", Path.cwd())
    # Set global user configurations
    nome = "" #TODO
    email = "" #TODO
    subprocess.run(["git", "config", "--global", "user.name", nome])
    subprocess.run(["git", "config", "--global", "user.email", email])
    generate_git_branches(params_file, num_years)
