from pathlib import Path

from loguru import logger
from torchvision.datasets import CIFAR10


def download_and_prepare_cifar10(path):
    download_to_path = Path(path)
    download_to_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"download_to_path directory is: {download_to_path.absolute()}")

    CIFAR10(root=path, train=True, download=True)
    logger.info("Finished downloading images")


if __name__ == "__main__":
    download_and_prepare_cifar10("data/cifar10")
