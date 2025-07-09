from pathlib import Path
from tqdm import tqdm
from loguru import logger
from torchvision import datasets
from torchvision import transforms
from torchvision.utils import save_image
import shutil
from .utils import is_already_downloaded, register_is_downloaded


def download_and_prepare_cifar10(download_to_path: Path) -> None:
    download_to_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"download_to_path directory is: {download_to_path.absolute()}")
    if not is_already_downloaded(download_to_path):
        temp_dir = download_to_path / "tmp"
        dataset = datasets.CIFAR10(root=temp_dir, train=True, download=True)
        
        class_names = dataset.classes  # ['airplane', 'automobile', ..., 'truck']

        # Create subfolders for each class
        for class_name in class_names:
            (download_to_path / class_name).mkdir(parents=True, exist_ok=True)

        # Save images in correct subfolder based on the class
        for idx, (img, label) in tqdm(enumerate(dataset), total=len(dataset)):
            class_name = class_names[label]
            filename = f"cifar10_{idx:05d}.png"
            to_tensor = transforms.ToTensor()
            tensor_image = to_tensor(img)
            save_image(tensor_image, download_to_path / class_name / filename)

        print(f"Saved {len(dataset)} images in '{download_to_path}' with subfolders per class.")
        

        shutil.rmtree(temp_dir / "cifar-10-batches-py")
        register_is_downloaded(download_to_path)


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent.parent.parent / "data/cifar10"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_cifar10("data/cifar10")
