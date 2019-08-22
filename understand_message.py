
from fuzzywuzzy import fuzz, process
#from metrics_ask import Metrics_Doctor
#from definition_ask import Definition_Doctor
#from subscription_ask import Subscription_Doctor


class Professor_X(object):
    def __init__(self, message_text):
        self.text = message_text
        self.initial_word = ['hi', 'hello', 'hey', 'help', 'get started']
        
    
    def memory_brain(self):
        file = open('memory_file.txt', 'w')
    	file.close()
        # check initial memory
        file_r = open('memory_file.txt', 'r')
        my_memory = file_r.read()
        
        if process.extractOne(self.text, self.initial_word, scorer = fuzz.ratio)[1] >= 80:
            file_w = open('memory_file.txt', 'w')
            file_w.write('')
            file_w.close()
        elif any(self.text in i for i in ['Metrics Value', 'Metrics Definition', 'Subscription Setting']):
            file_w = open('memory_file.txt', 'w')
            file_w.write(self.text)
            file_w.close()
        elif any(my_memory in i for i in ['Metrics Value', 'Metrics Definition', 'Subscription Setting']):
            pass
        else:
            file_w = open('memory_file.txt', 'w')
            file_w.write('')
            file_w.close()
            
        file_r = open('memory_file.txt', 'r')
        my_memory = file_r.read()

        return my_memory

    def get_reply(self):
        memory = self.memory_brain()
        print('the current memory:' + memory)
    
        #clean_text = process.extractOne(self.text, initial_word, scorer = fuzz.ratio)[0]

        if memory == 'Metrics Value':
            #reply_message = Metrics_Doctor(self.text).get_reply_message()
            reply_message = {
                'message_format': 'text',
                'text': 'Hey I know you are asking me about Definition'
            }

        elif memory == 'Metrics Definition':
            #reply_message = Definition_Doctor(self.text).get_reply_message()
            reply_message = {
                    'message_format': 'text',
                    'text': 'Hey I know you are asking me about Definition'
            }

        elif memory == 'Subscription Setting':
            #reply_message = Subscription_Doctor(self.text).get_reply_message()
            reply_message = {
                    'message_format': 'text',
                    'text': 'Hey I know you are asking me about Subscription'
            }


        elif memory == '':
            # reply intial button message
            button_type = ['postback', 'postback', 'postback']
            button_title = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
            button_payload = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
            button_text = 'Hi, what would you like to get from me?'
            reply_message = {
                    'message_format': 'button',
                    'type': button_type,
                    'title': button_title,
                    'payload': button_payload,
                    'text': button_text
            }


        return reply_message
