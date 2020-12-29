import os
import pytest
from image_uploader import ImageUploader, ImageUploaderError


class TestImageUploader:

    def test_get_file_error(self):
        uploader = ImageUploader("http://example.com", "/")
        with pytest.raises(ImageUploaderError) as err:
            _ = uploader._get_file("test.jpg")
        assert str(err.value) == "Can't open file: [Errno 2] No such file or directory: 'test.jpg'"

    def test_get_only_image(self):
        uploader = ImageUploader("http://example.com", os.path.join(os.getcwd(), "test", "test_data"))
        images = uploader._get_images_from_dir()
        assert len(images) == 1
        assert os.path.split(images[0])[1] == "IMG_20160731_100456.jpg"
