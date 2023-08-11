from app.main import app
from fastapi.testclient import TestClient
from faker import Faker

client = TestClient(app)
fake_data = Faker()


'''----------- Test ping --------------------'''
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == 'pong'


'''----------- Test upload --------------------'''

def test_upload_manual_miss_date():
    img_data = {
        "field_id": fake_data.random_number(1),
        "lat": fake_data.random_number(3),
        "lon": fake_data.random_number(3),
        "dim": fake_data.random_number(3),
    }

    response = client.post("/save-images-manual", json=img_data)

    assert response.status_code == 200


def test_upload_manual_miss_id():
    img_data = {
        "lat": fake_data.random_number(3),
        "lon": fake_data.random_number(3),
        "dim": fake_data.random_number(3),
    }
    response = client.post("/save-images-manual", json=img_data)
    assert response.status_code == 422

def test_upload_manual_big_nummber():
    img_data = {
        "field_id": fake_data.random_number(1),
        "lat": fake_data.random_number(100),
        "lon": fake_data.random_number(100),
        "dim": fake_data.random_number(100),
        "date": fake_data.date()
    }
    response = client.post("/save-images-manual", json=img_data)
    assert response.status_code == 408

def test_upload_file_200():

    test_file = 'example_info_nasa_earth.csv'
    files = {'file': ('test_file.docx', open(test_file, 'rb'))}
    response = client.post('save-images-uploadfile', files=files)
    assert response.status_code == 200

def test_upload_file_none():
    test_file = ''
    files = {'file': ('test_file.docx', open(test_file, 'rb'))}
    response = client.post('save-images-uploadfile', files=files)
    assert response.status_code == 200
