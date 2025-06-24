from enum import Enum
from pathlib import Path

from loguru import logger

from .download_cifar10 import download_and_prepare_cifar10
from .download_rsna import download_and_prepare_rsna
from .download_taco import download_and_prepare_taco
from .download_trashnet import download_and_prepare_trashnet


class DatasetType(Enum):
    CIFAR10 = 1
    TACO = 2
    TRASHNET = 3
    RSNA = 4


class DatasetDownloader:
    @staticmethod
    def create(dataset_type: DatasetType, dataset_path: Path) -> None:
        logger.info(
            f"Creating dataset downloader for {dataset_type.name} at {dataset_path}"
        )
        download_to = dataset_path / dataset_type.name

        download_to.mkdir(parents=True, exist_ok=True)
        logger.info(f"Download to directory is: {download_to.absolute()}")

        creators = {
            DatasetType.TACO: lambda: download_and_prepare_taco(download_to),
            DatasetType.TRASHNET: lambda: download_and_prepare_trashnet(download_to),
            DatasetType.CIFAR10: lambda: download_and_prepare_cifar10(download_to),
            DatasetType.RSNA: lambda: download_and_prepare_rsna(download_to),
        }

        if dataset_type not in creators:
            raise ValueError(f"Dataset '{dataset_type.name}' not supported.")

        return creators[dataset_type]()


# python -m hu_datasets.DatasetDownloader to run the script directly
if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent / "data"
    logger.info(f"Download directory is: {download_directory.absolute()}")

    # Example usage
    DatasetDownloader.create(DatasetType.TACO, download_directory)
    # DatasetDownloader.create(DatasetType.TRASHNET, download_directory)
    # DatasetDownloader.create(DatasetType.CIFAR10, download_directory)
    # DatasetDownloader.create(DatasetType.RSNA, download_directory)
