from pathlib import Path

from loguru import logger
from torchvision import datasets
from DatasetDownloader import is_already_downloaded, register_is_downloaded


def download_and_prepare_cifar10(download_to_path: Path) -> None:
    download_to_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"download_to_path directory is: {download_to_path.absolute()}")
    if not is_already_downloaded(download_to_path): 
        datasets.CIFAR10(root=download_to_path, train=True, download=True)
        register_is_downloaded(download_to_path)


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent.parent.parent / "data/cifar10"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_cifar10("data/cifar10")
