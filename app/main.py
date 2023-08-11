import codecs
import csv
from app.core.upload_file import upload_file
from app.models.models import ImageryErath
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    BackgroundTasks
)
app = FastAPI()


@app.get("/ping")
async def root():
    '''
    Helty  endpoint
    :return:
    '''
    return "pong"

@app.post("/save-images-manual/")
async def save_manul_img(imagery_erath: ImageryErath):
    '''
    Consult manualy a specific images and save in s3 bucket
    :param item:
    :return:
    '''
    upload_file_msg = upload_file([dict(imagery_erath)])
    return imagery_erath


@app.post("/save-images-uploadfile/")
async def create_upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    '''
    Consult a list params in csv for save in bucket s3
    :param background_tasks:
    :param file:
    :return:
    '''
    if file.size == 0:
        return "File empty"

    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    background_tasks.add_task(file.file.close)
    upload_file_msg = upload_file(list(csvReader))
    return upload_file_msg


@app.get("/list-images")
async def say_hello(name: str):
    '''
    get the s3 rute for each images
    :param name:
    :return:
    '''
    return {"message": []}