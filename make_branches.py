import datetime
import subprocess
import yaml
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


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
def create_git_branch(
    params_file: str, start_date: datetime.datetime, end_date: datetime.datetime
):
    """
    Creates a git branch for a given params file and date range.

    Args:
        params_file: The name of the params file.
        start_date: The start date of the date range.
        end_date: The end date of the date range.
    """

    # Get the name of the current branch
    main_branch = (
        subprocess.run(["git", "branch", "--show-current"], capture_output=True)
        .stdout.decode("utf-8")
        .strip()
    )

    runs = list()

    branch_name = f"multirrotulo-train-{start_date.year}"

    # Checkout a new branch
    logger.info(f"Creating branch {branch_name}")
    runs.append(
        True
        if subprocess.run(["git", "checkout", "-b", branch_name]).returncode == 0
        else False
    )

    # Update the params file
    update_params_file(params_file, start_date, end_date)

    logger.info(f"Adding {params_file} to branch {branch_name}")
    runs.append(
        True if subprocess.run(["git", "add", params_file]).returncode == 0 else False
    )

    logger.info(f"Commiting {params_file} to branch {branch_name}")
    runs.append(
        True
        if subprocess.run(
            ["git", "commit", "-m", f"Add {branch_name} version of params.yml"]
        ).returncode
        == 0
        else False
    )

    # logger.info(f"Pushing {branch_name} to directory")
    logger.info(f"Pushing {branch_name} to remote")
    runs.append(
        True
        if subprocess.run(["git", "push", "origin", branch_name]).returncode == 0
        else False
    )
    # destination_repo = f"/home/modelsbi/data/triagem/{branch_name}"
    # logger.info(f"Cloning {branch_name} to {destination_repo}")
    # runs.append(
        # True
        # if subprocess.run(["git", "clone", ".", destination_repo]).returncode == 0
        # else False
        # )
    # logger.info(f"Branch {branch_name} created in {destination_repo}")

    # Checkout main branch
    logger.info(f"Checking out {main_branch}")
    runs.append(
        True
        if subprocess.run(["git", "checkout", main_branch]).returncode == 0
        else False
    )

    return all(runs)


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


def generate_git_branches(params_file: str, num_years: int) -> None:
    """
    Create a branch for each year between the start date and the start date minus the number of years.
    Each branch will have a name corresponding to the year.

    Args:
        params_file (str): The name of the params file.
        start_date (datetime.datetime): The start date for the first branch.
        num_years (int): The number of branches to create.
    """

    logger.info(f"Generating {num_years} branches")

    # Get the start date for the current iteration
    start_date = get_date("data-inicio-treino")
    logger.info(f"Getting start date for branch {start_date.year}")

    # Get the end date for the current iteration
    end_date = get_date("data-fim-treino")
    logger.info(f"Getting end date for branch {end_date.year}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_branches = {
            executor.submit(create_git_branch, params_file, start, end): (start, end)
            for _, (start, end) in enumerate(
                zip(
                    (
                        start_date.replace(year=start_date.year - i)
                        for i in range(num_years)
                    ),
                    (
                        end_date.replace(year=end_date.year - i)
                        for i in range(num_years)
                    ),
                )
            )
        }
        for future in as_completed(future_to_branches):
            start, end = future_to_branches[future]
            # Verifique se a criação da branch foi concluída com sucesso
            try:
                run = future.result()
            except Exception as exc:
                print(f"Criação da branch '{(start.year, end.year)}' falhou: {exc}")
            else:
                if run:
                    logger.info(f"Branch {(start.year, end.year)} criada com sucesso")
                else:
                    logger.error(f"Branch {(start.year, end.year)} falhou")


# Execução
# params_file is the name of the file with the parameters of the simulation
# start_date is the date of the first commit
# num_years is the number of years to simulate
if __name__ == "__main__":
    logger.info("Workdir: %s", Path.cwd())
    main_branch = (
        subprocess.run(["git", "branch", "--show-current"], capture_output=True)
        .stdout.decode("utf-8")
        .strip()
    )
    generate_git_branches(params_file, num_years)

    subprocess.run(["git", "checkout", main_branch])
