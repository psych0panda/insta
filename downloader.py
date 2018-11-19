import json
import uuid
import requests


class Downloader:
    media = []

    def __init__(self, logger: object,
                 api: object,
                 pk: object = '1902334525193445278',
                 username: object = 'kay.daniilovna') -> object:
        self.logger = logger
        self.api = api
        self.pk = pk
        self.username = username

    def run(self)-> None:
        results = self.api.username_feed(self.username)
        urls_list = []
        urls_list.extend(results.get('items', []))
        next_max_id = results.get('next_max_id')
        while next_max_id:
            results = self.api.username_feed(self.username, max_id=next_max_id)
            urls_list.extend(results.get('items', []))
            next_max_id = results.get('next_max_id')

        for i in urls_list:
            candidates = i.get('image_versions2')
            if type(candidates) is not dict:
                candidates = i.get('carousel_media')
                for _ in candidates:
                    carousel = _.get('image_versions2')
                    urls = carousel['candidates']
                    for url in urls:
                        self.download(url.get('url'))
            else:
                urls = candidates['candidates']
                for url in urls:
                    self.download(url.get('url'))

    @staticmethod
    def download(url, path: object= 'data/original/')-> None:
        r = requests.get(url)
        with open(path + str(uuid.uuid4()) + '.jpg', 'wb+') as f:
            f.write(r.content)

    @staticmethod
    def write_json(data: object, path: str='data.json')-> None:
        with open(path, 'w+', encoding='utf8') as w:
            w.write(json.dumps(data, ensure_ascii=False, indent=4))
