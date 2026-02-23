import tempfile
from PIL import Image
from io import BytesIO
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_blob() -> None:
    # Usar Fixtures
    # Não é antipadrao subir arquivos de vide/imagem no repo
    img_byte_arr = BytesIO()
    width = height = 128
    valid_solid_color_jpeg = Image.new(mode='RGB', size=(width, height), color='red')
    valid_solid_color_jpeg.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    files = [("test_file_red.jpg", img_byte_arr)]

    headers = {
        "Content-Type": "multipart/form-data"
    }
    response = client.put(
        "/v1/media/upload",
        headers=headers,
        files=files
    )



def test_get_blob_by_name() -> None:
    response = client.get("/v1/media/test_file_red.jpg")
    assert response.status_code == 200
    # assert response.json() == {
    #    "name": "media-processing/938.zip",
	#    "created_at": "2025-12-02T17:40:06.553291Z",
	#    "updated_at": "2025-12-02T17:40:06.553328Z",
	#    "download_url": "http://0.0.0.0:4443/bkt-media-processing-local/media-processing/938.zip"
    # }
