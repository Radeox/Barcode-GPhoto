import logging
from pathlib import Path

import gphoto2 as gp
from PIL import Image

gp.error_severity[gp.GP_ERROR] = logging.WARNING


class Camera:
    def __init__(self) -> None:
        try:
            self.camera = gp.Camera()
            self.camera.init()
        except gp.GPhoto2Error as ex:
            print(f"Error: {ex}")
            exit(1)

    def __enter__(self) -> "Camera":
        return self

    def __exit__(self, _, __, ___) -> None:
        print("Exiting camera...")
        self.camera.exit()

    def __set_single_config(self, config: str, new_value: str) -> None:
        """
        Set the value of specific config, or None on error
        """

        new_config = self.camera.get_single_config(config)
        new_config.set_value(new_value)
        self.camera.set_single_config(config, new_config)

    def capture_photo(self, destination: str = "output") -> list:
        """
        Capture a photo in JPEG and RAW format
        """

        # Set drive mode
        self.__set_single_config("drivemode", "Single")
        #
        # # Keep on memory card
        self.__set_single_config("capturetarget", "Internal RAM")
        #
        # # Set image format
        self.__set_single_config("imageformat", "RAW + Large Fine JPEG")

        # Capture images
        self.__set_single_config("eosremoterelease", "Immediate")

        # Release shutter
        self.__set_single_config("eosremoterelease", "Release Full")

        # We wait until JPEG and RAW has been transferred
        files = []

        while True:
            type_, file = self.camera.wait_for_event(60 * 1000)  # 60 seconds
            if type_ == gp.GP_EVENT_CAPTURE_COMPLETE or type_ == gp.GP_EVENT_TIMEOUT:
                # We're done here
                break
            elif type_ == gp.GP_EVENT_FILE_ADDED:
                # Save photo
                img = self.camera.file_get(
                    file.folder, file.name, gp.GP_FILE_TYPE_NORMAL
                )

                # Save image
                path = Path(destination)
                img.save(str(path.joinpath(file.name)))

                # Add file to list
                files.append(file.name)
                if len(files) == 2:
                    break

        return files


def main():
    print("Barcode - GPhoto\n================\n")
    output_dir = Path("output")
    output_file = output_dir.joinpath("barcodes.txt")

    # Create output dir if missing
    if output_dir.exists() is False:
        output_dir.mkdir()

    # Create output file if missing
    if output_file.exists() is False:
        output_file.touch()

    while True:
        try:
            prefix = input("Enter prefix for the photo: ")

            # Capture photos
            with Camera() as camera:
                photos = camera.capture_photo(str(output_dir))

            # Rename each photo with the prefix
            for photo in photos:
                print(f"Renaming {photo} to {prefix}_{photo}")
                photo_path = output_dir.joinpath(photo)
                photo_path.rename(photo_path.with_name(f"{prefix}_{photo}"))
                photo_path = photo_path.with_name(f"{prefix}_{photo}")

                # Open preview
                if photo.endswith(".jpg"):
                    with Image.open(str(photo_path)) as img:
                        img.show()

            # Read old barcodes
            barcodes = []
            with open(str(output_file), "r") as file:
                barcodes = file.readlines()
                barcodes = [barcode.strip() for barcode in barcodes]

            # Save new barcode
            barcodes.append(prefix)
            barcodes = set(barcodes)
            with open(str(output_file), "w") as file:
                for barcode in barcodes:
                    file.write(f"{barcode}\n")

        except KeyboardInterrupt:
            del camera
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
