from pathlib import Path


class Config:
    """The Config class contains configuration which is used to configure classes in the container."""

    # The file in which general CLI configuration is stored
    general_config_file = Path("~/.lean/credentials").expanduser()

    # The file in which credentials are stored
    credentials_config_file = Path("~/.lean/credentials").expanduser()

    # The default name of the configuration file in a Lean CLI project
    default_lean_config_file_name = "lean.json"

    # The default name of the data directory in a Lean CLI project
    default_data_directory_name = "data"

    # The Docker image used when running the LEAN engine locally
    lean_engine_docker_image = "quantconnect/lean"

    # The tag of the Docker image used when running the LEAN engine locally
    lean_engine_docker_tag = "latest"

    # The base url of the QuantConnect API
    api_base_url = "https://www.quantconnect.com/api/v2"
