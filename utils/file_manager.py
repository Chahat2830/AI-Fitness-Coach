from pathlib import Path


class FileManager:

    @staticmethod
    def save_uploaded_image(uploaded_file, save_path):

        save_path = Path(save_path)

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())