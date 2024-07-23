packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "python-dotenv",
]

basic = [
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "numpy",
    "pandas",
    "scikit-learn",
    "ploomber",
    "boto3"
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
]

r_dependencies = [
    "r-base",
    "r-irkernel",
    "r-dotenv"
]


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version,
    environment_manager, include_r_kernel
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["" "-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {p}" for p in packages if p not in pip_only_packages]

            if include_r_kernel == "Yes" and environment_manager == "conda":
                lines += [f"  - {r_dep}" for r_dep in r_dependencies]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))

    elif dependencies == "Pipfile":
        with open(dependencies, "w") as f:
            lines = ["[packages]"]
            lines += [f'{p} = "*"' for p in sorted(packages)]

            lines += [f'"{module_name}" ={{editable = true, path = "."}}']

            lines += ["", "[requires]", f'python_version = "{python_version}"']

            f.write("\n".join(lines))
