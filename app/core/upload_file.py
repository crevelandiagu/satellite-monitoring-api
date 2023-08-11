import os
import mimetypes
from datetime import date
from app.aws.aws_client import AwsClient
from app.adapters.http_client import HTTPClient

class NasaHttClient(HTTPClient):
    def __init__(self):
        self.key_nasa_earth = os.getenv('KEY_NASA_EARTH', '')
        super(NasaHttClient, self).__init__()

    def generate_url(self,url_key , *args, **kwargs):
        '''
        Generate any url you need used for nasa's api
        :param args:
        :param kwargs:
        :return:
        '''
        lon = kwargs['lon']
        lat = kwargs['lat']
        date = kwargs['date']
        dim = kwargs['dim']
        factory_url = {
            "earth": f'https://api.nasa.gov/planetary/earth/imagery?lon={lon}&dim={dim}&lat={lat}&date={date}&api_key={self.key_nasa_earth}',
            'earth_assets': '',
        }
        url = factory_url.get(url_key)
        if not url:
            raise ValueError(f"URL key '{url_key}' not found")
        return url


def upload_file(data_image: list):
    '''
    Upload file to s3 with
    s3://{BUCKET_NAME}/{field_id}/{date}_imagery.png`

    :param data_image: list of dictionary with information imagen to get for nasa
    :return:
    '''

    s3 = AwsClient.s3_client()
    try:
        nasa_client = NasaHttClient()
        for nasa_info_require in data_image:
            urls_images = nasa_client.generate_url('earth', **nasa_info_require)
            image_response = nasa_client.get(urls_images)
            content_type = image_response.headers['content-type']
            extension = mimetypes.guess_extension(content_type)

            file_name = f'{nasa_info_require.get("date", "")}_imagery'
            if not nasa_info_require.get('date') or nasa_info_require.get('date') == '':
                file_name = f'{date.today().strftime("%Y-%m-%d")}_imagery'

            bucket = f"{os.getenv('BUCKET_NAME','')}/{nasa_info_require.get(nasa_info_require,'')}"
            s3.upload_fileobj(image_response, bucket, file_name + extension)

        print("Upload Successful")
        return 'Upload Successful'
    except FileNotFoundError:
        print("The file was not found")
        return 'The file was not found'
    except Exception as e:
        print(f'Error aws {e}')
        return f'Error aws {e}'
