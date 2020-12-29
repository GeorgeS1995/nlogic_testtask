import http.client
import mimetypes
import os
from typing import Tuple, Union
from urllib import parse
from pprint import pprint
import argparse


class ImageUploaderError(Exception):
    pass


class ImageUploader:
    IMG_EXT = {".gif", ".jpeg", ".jpg", ".png", ".svg"}

    def __init__(self, url, img_dir):
        self.url = parse.urlparse(url)
        self.img_dir = img_dir
        self.conn = http.client.HTTPSConnection if self.url.scheme == "https" else http.client.HTTPConnection

    def _get_mimetype(self, img: str) -> str:
        return mimetypes.types_map[os.path.splitext(img)[1]]

    def _get_file(self, img: str) -> Tuple[bytes, str]:
        try:
            with open(img, "rb") as f:
                return f.read(), self._get_mimetype(img)
        except OSError as err:
            raise ImageUploaderError(f"Can't open file: {err}")

    def _get_connection(self) -> Union[http.client.HTTPConnection, http.client.HTTPSConnection]:
        try:
            return self.conn(self.url.netloc)
        except http.client.HTTPException as err:
            pprint(f"Can't connect to resource: {err}")
            exit(1)

    def _upload(self, img: str):
        try:
            payload, mimetype = self._get_file(img)
        except ImageUploaderError as err:
            pprint(err)
            return
        headers = {
            'Content-Type': mimetype,
            'Content-Disposition': f'attachment; filename={os.path.split(img)[1]}'
        }

        connection = self._get_connection()
        connection.request("POST", "/images", payload, headers)
        try:
            r = connection.getresponse()
        except ConnectionResetError as err:
            pprint(f"Response error while uploading {img}: {err}")
            return
        if r.status != 200:
            pprint(f"Can't upload file {img}, resource response: {r.read()}")
            return
        pprint(f'File {img} successfully uploaded!')

    def _get_images_from_dir(self) -> list:
        return [os.path.join(self.img_dir, img) for img in os.listdir(self.img_dir)
                if os.path.splitext(img)[1] in self.IMG_EXT]

    def upload(self):
        if not os.path.isdir(self.img_dir):
            pprint(f"It's not a directory: {self.img_dir}")
            exit(1)
        images = self._get_images_from_dir()
        for i in images:
            self._upload(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, nargs='?', required=True)
    parser.add_argument('--dir', type=str, nargs="?", required=True)
    args = parser.parse_args()
    uploader = ImageUploader(args.server, args.dir)
    uploader.upload()
