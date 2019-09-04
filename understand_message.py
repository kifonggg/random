
from fuzzywuzzy import fuzz, process
from metrics_ask import Metrics_Doctor
#from definition_ask import Definition_Doctor
#from subscription_ask import Subscription_Doctor


class Professor_X(object):
    def __init__(self, message_text):
        self.text = message_text
        self.initial_word = ['hi', 'hello', 'hey', 'help', 'get started']
        self.end_word = ['thanks', 'bye', 'thank you', 'good', 'ok']


        
    
    def memory_brain(self):

    	# check initial memory
        try:
            file_r = open('memory_file.txt', 'r')
            my_memory = file_r.read()
        except:
            file_ = open('memory_file.txt', 'w')
            file_.close()
            file_r = open('memory_file.txt', 'r')
            my_memory = file_r.read()
        
        if process.extractOne(self.text, self.initial_word, scorer = fuzz.ratio)[1] >= 80:
            file_w = open('memory_file.txt', 'w')
            file_w.write('')
            file_w.close()
        elif process.extractOne(self.text, self.end_word, scorer = fuzz.ratio)[1] >= 80:
            file_w = open('memory_file.txt', 'w')
            file_w.write('end')
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
        print('Professor_X current memory:' + memory)
    
        #clean_text = process.extractOne(self.text, initial_word, scorer = fuzz.ratio)[0]

        if memory == 'Metrics Value':
            reply_message = Metrics_Doctor(self.text).get_reply_message()
            

        elif memory == 'Metrics Definition':
            #reply_message = Definition_Doctor(self.text).get_reply_message()
            reply_message = {
                    'message_format': 'text',
                    'text': 'Hey I know you are asking me about Definition. Unfortunely, this service it not available yet. Please stay tuned for it. =)\n'+
                            'Say "Hi" to me for restarting the process.'
            }

        elif memory == 'Subscription Setting':
            #reply_message = Subscription_Doctor(self.text).get_reply_message()
            reply_message = {
                    'message_format': 'text',
                    'text': 'Hey I know you are asking me about Subscription. Unfortunely, this service it not available yet. Please stay tuned for it. =)\n'+
                            'Say "Hi" to me for restarting the process.'
            }

        elif memory == 'end':
            reply_message = {
                    'message_format': 'text',
                    'text': 'Thank you for looking for me. Just Say "Hi" to me when you need help.\n'+
                            'Hope to see you again. =)'
            }

        elif memory == '':
            # reply intial button message
            button_type = ['postback', 'postback', 'postback']
            button_title = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
            button_payload = ['Metrics Value', 'Metrics Definition', 'Subscription Setting']
            button_text = 'Hi, how would you like to help you?'
            reply_message = {
                    'message_format': 'button',
                    'type': button_type,
                    'title': button_title,
                    'payload': button_payload,
                    'text': button_text
            }


        return reply_message
