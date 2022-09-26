# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import List

from lean.components.config.lean_config_manager import LeanConfigManager
from lean.components.config.project_config_manager import ProjectConfigManager
from lean.components.util.path_manager import PathManager
from lean.models.utils import LeanLibraryReference


class LibraryManager:
    """The LibraryManager class provides utilities for handling a libraries."""

    def __init__(self,
                 project_config_manager: ProjectConfigManager,
                 lean_config_manager: LeanConfigManager,
                 path_manager: PathManager) -> None:
        """Creates a new LibraryManager instance.

        :param project_config_manager: the ProjectConfigManager to use when creating new projects
        :param lean_config_manager: the LeanConfigManager to get the CLI root directory from
        :param path_manager: the path manager to use to handle library paths
        """
        self._project_config_manager = project_config_manager
        self._lean_config_manager = lean_config_manager
        self._path_manager = path_manager

    def is_lean_library(self, path: Path) -> bool:
        """Checks whether the library name is a Lean library path

        :param path: path to check whether it is a Lean library
        :return: true if the path is a Lean library path
        """
        if not self._path_manager.is_path_valid(path):
            return False

        relative_path = self._path_manager.get_relative_path(path, self._lean_config_manager.get_cli_root_directory())
        path_parts = relative_path.parts
        library_config = self._project_config_manager.get_project_config(path)
        library_language = library_config.get("algorithm-language", None)

        return (
            len(path_parts) > 0 and
            path_parts[0] == "Library" and
            relative_path.is_dir() and
            library_language is not None
        )

    def get_csharp_lean_library_path_for_csproj_file(self, project_dir: Path, library_dir: Path) -> Path:
        """Gets the library path to be used for the project's .csproj file.

        The returned path is relative to the project directory so auto complete can be provided.

        :param project_dir: The path to the project directory
        :param library_dir: The path to the library directory
        :return The path to be used for the project's .csproj file
        """
        cli_root_dir = self._lean_config_manager.get_cli_root_directory()
        project_dir_relative_to_cli = self._path_manager.get_relative_path(project_dir, cli_root_dir)
        library_dir_relative_to_cli = self._path_manager.get_relative_path(library_dir, cli_root_dir)
        library_csproj_file = self.get_csproj_file_path(library_dir_relative_to_cli)
        library_csproj_file = "../" * len(project_dir_relative_to_cli.parts) / library_csproj_file

        return library_csproj_file

    def get_library_path_for_project_config_file(self, library_dir: Path) -> Path:
        """Gets the library path to be used for the project's config.json file.

        :param library_dir: The path to the library directory
        :return The path to be used for the project's config.json file
        """
        lean_cli_root_dir = self._lean_config_manager.get_cli_root_directory()
        return self._path_manager.get_relative_path(library_dir, lean_cli_root_dir)

    @staticmethod
    def get_csproj_file_path(project_dir: Path) -> Path:
        """Gets the path to the csproj file in the project directory.

        :param project_dir: Path to the project directory
        :return: Path to the csproj file in the project directory
        """
        return next(p for p in project_dir.iterdir() if p.name.endswith(".csproj"))
