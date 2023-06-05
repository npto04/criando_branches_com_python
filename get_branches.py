import os
from time import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_branch_name(year):
    branch_name = f"params_{year}"
    return branch_name

def clone(year, base_directory, remote_repo):
    # Obtenha o nome da branch
    branch_name = get_branch_name(year)
    
    directory = os.path.join(base_directory, str(year))

    # Clone a branch específica para o diretório correspondente
    run = subprocess.run(["git", "clone", "--branch", branch_name, remote_repo, directory])

    return run

# Defina as variáveis do repositório remoto
remote_repo = "https://github.com/npto04/criando_branches_com_python"
base_directory = "tmp"
start = time()
with ThreadPoolExecutor() as executor:
    future_to_clones = {executor.submit(clone, year, base_directory, remote_repo): year for year in range(2019, 2007, -1)}
    for future in as_completed(future_to_clones):
        year = future_to_clones[future]
        # Verifique se a clonagem foi concluída com sucesso
        try:
            run = future.result()
        except Exception as exc:
            print(f"Clonagem da branch '{year}' falhou: {exc}")
        else:
            if run.returncode == 0:
                print(f"Clonagem da branch '{year}' concluída com sucesso!")
            else:
                print(f"Falha ao clonar a branch '{year}'. Verifique se a branch existe e se a URL do repositório está correta.")
end = time()


