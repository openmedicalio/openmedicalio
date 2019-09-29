import requests, json, time, copy, os
from pathlib import Path

dot = Path(__file__).parent
default_model_name = '774M'


class Client():
    def __init__(self, key):
        self.key = key
        self.timeout = 1e9
        self.url1 = 'https://us-central1-project-318531836785902414.cloudfunctions.net/auth'
        self.url2 = 'https://us-central1-project-318531836785902414.cloudfunctions.net/status'
        self.session = requests.Session()

    # def fast_generate(self,
    #                   prompt,
    #                   model_name=default_model_name,
    #                   ):
    #     kwargs = copy.deepcopy(locals())
    #     del kwargs['self']
    #     return self.generate(**kwargs, shared=True)

    def generate(self,
                 prompt='',
                 model_name=default_model_name,
                 nsamples=None,
                 length=None,
                 temperature=None,
                 top_k=None,
                 ):
        # nsamples_max = 15
        # length_max = 200
        # assert nsamples < nsamples_max, f'nsamples must be less than {nsamples_max}'
        # if shared:
        #     assert length < length_max, f'length must be less than {length_max}'

        prompt = prompt.strip(' ')
        kwargs = copy.deepcopy(locals())
        kwargs = dict((x for x in kwargs.items() if x[1] is not None))
        del kwargs['self']
        return self._send_message('generate', kwargs=kwargs)

    def finetune(self,
                 target_model_name,
                 dataset_path='',
                 base_model_name=default_model_name,
                 upload=True,
                 steps=500,
                 ):
        if target_model_name == default_model_name:
            print(f'Cannot overwrite default model {default_model_name}.')
            raise AssertionError
        dataset_name = os.path.basename(dataset_path)
        if upload:
            dataset = Path(dataset_path).read_text()
        kwargs = copy.deepcopy(locals())
        del kwargs['self']
        return self._send_message('finetune', kwargs=kwargs)

    def entities(self, q):
        kwargs = copy.deepcopy(locals())
        del kwargs['self']
        return self._send_message('entities', kwargs=kwargs)

    def _send_message(self, method, kwargs):
        print(method)
        print(kwargs)
        data = {}
        data['key'] = self.key
        data['kwargs'] = kwargs
        data['method'] = method
        data['result'] = ''
        data['tag'] = ''
        # data['charge'] = True
        data['status'] = 'pending'
        data['messages'] = []
        data['bids'] = []

        r = self.session.post(url=self.url1, json=data, ).json()
        # r = self.session.post(url=url, json=load1, ).json()

        t = 0
        dt = 1
        while True:
            # while t < self.timeout:
            result = r['result']
            status = r['status']
            messages = ('\n'.join(r['messages']))
            if messages:
                print(messages)
            if status in ['done', 'failed']:
                print(f'Status: {status}')
                if status == 'done':
                    if method=='entities':
                        result=json.loads(result)

                    print(f'Result\n{result}\n')
                    return result
                elif status == 'failed':

                    raise AssertionError

            r = self.session.post(url=self.url2, json={'id': r['id']}, ).json()
            time.sleep(dt)
            t += dt


if __name__ == '__main__':
    pass