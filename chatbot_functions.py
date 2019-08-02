import time
import hmac
import hashlib
import requests

class coolbot():

    graph_url = 'https://graph.facebook.com'
    message_url = '/v3.3/me/messages'
    
    
    def __init__(self, access_token, app_secret):
        self.access_token = access_token
        self.app_secret = app_secret
    

    def query_string(self):
        app_time = round(time.time()-10)
        appsecret_proof = hmac.new(self.app_secret.encode('utf-8'), msg=(self.access_token + '|' + str(app_time)).encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        self._query_string = {"appsecret_proof":appsecret_proof,
                       "access_token":self.access_token,
                       "appsecret_time":app_time}
        return self._query_string

    
    def send_message(self, recipient_id, message, message_type):
        result = []
        if type(recipient_id) == str:
            if message_type == 'thread':
                payload = {
                    'recipient': {'thread_key': recipient_id},
                    'message': message
                }
            elif message_type == 'message':
                payload = {
                    'recipient': {'id': recipient_id},
                    'message': message
                }

            return self.send_raw(payload)
        elif type(recipient_id) == list:
            for i in range(len(recipient_id)):
                if message_type == 'thread':
                    payload = {
                        'recipient': {'thread_key': recipient_id[i]},
                        'message': message
                    }
                elif message_type == 'message':
                    payload = {
                        'recipient': {'id': recipient_id[i]},
                        'message': message
                    }
                result_from_raw = (self.send_raw(payload))
                result.append(result_from_raw)
                
            return result
                

    def send_text_message(self, recipient_id, message, message_type):

        return self.send_message(recipient_id, {'text': message}, message_type)

    def send_attachement(self, recipient_id, attachement_type, attachment_path, message_type):
        result = []
        if type(recipient_id) == str:
            if message_type == 'thread':
                payload = {
                    'recipient': str({'thread_key': recipient_id}),
                    'message': str({'attachment': {'type': attachement_type,'payload': {} }  }),
                    'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'), 'image/png')
                }
                multipart_data = MultipartEncoder(payload)
                multipart_header = {'Content-Type': multipart_data.content_type}

            elif message_type == 'message':

                payload = {
                    'recipient': str({'id': recipient_id}),
                    'message': str({'attachment': {'type': attachement_type,'payload': {} }  }),
                    'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'), 'image/png')
                }
                multipart_data = MultipartEncoder(payload)
                multipart_header = {'Content-Type': multipart_data.content_type}
            return requests.post(self.graph_url + self.message_url, data=multipart_data, params=self.query_string(), headers=multipart_header).json()
        elif type(recipient_id) == list:
            for i in range(len(recipient_id)):
                if message_type == 'thread':
                    payload = {
                        'recipient': str({'thread_key': recipient_id[i]}),
                        'message': str({'attachment': {'type': attachement_type,'payload': {} }  }),
                        'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'), 'image/png')
                    }
                    multipart_data = MultipartEncoder(payload)
                    multipart_header = {'Content-Type': multipart_data.content_type}

                elif message_type == 'message':

                    payload = {
                        'recipient': str({'id': recipient_id[i]}),
                        'message': str({'attachment': {'type': attachement_type,'payload': {} }  }),
                        'filedata': (os.path.basename(attachment_path), open(attachment_path, 'rb'), 'image/png')
                    }
                    multipart_data = MultipartEncoder(payload)
                    multipart_header = {'Content-Type': multipart_data.content_type}
                res = requests.post(self.graph_url + self.message_url, data=multipart_data, params=self.query_string(), headers=multipart_header).json()
                result.append(res)
            return result
            
    def send_raw(self, payload):
        response = requests.post(url = self.graph_url + self.message_url, params=self.query_string(), json=payload)
        result = response.json()

        return result
    
    def check_error(self, result, notify_users):
        if 'error' in str(result):
            message_content = 'Error sending messgae to some recipient.\n'+'Error message: \n' + str(result)
            return self.send_text_message(recipient_id = notify_users, message_type = 'message'
                                  , message = message_content)
        
    def get_user_info(self, recipient_id, fields=None):
        # Useful fields options
        # ['id','first_name','last_name','email','title','organization','division','department','name']
        params = {}
        if fields is not None and isinstance(fields, (list, tuple)):
            params['fields'] = ",".join(fields)
            print(params)

        params.update(self.query_string())
        print(params)

        request_endpoint = '{0}/{1}'.format(self.graph_url, recipient_id)
        print(request_endpoint)
        response = requests.get(request_endpoint, params=params)
        print(response)
        if response.status_code == 200:
            return response.json()

        return None
