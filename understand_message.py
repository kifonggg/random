
from fuzzywuzzy import fuzz, process
#from metrics_ask import Metrics_Doctor
#from definition_ask import Definition_Doctor
#from subscription_ask import Subscription_Doctor


class Professor_X(object):
	def __init__(self, message_text):
		self.text = message_text
		initial_word = ['hi', 'hello', 'hey', 'help', 'get started']
		
	def memory_brain(self):

		global my_memory
		if any(my_memory in i for i in ['Metrics Value', 'Metrics Definition', 'Subscription Setting']):
			my_memory = my_memory

		if any(self.text in i for i in ['Metrics Value', 'Metrics Definition', 'Subscription Setting']):
			my_memory = self.text
		elif process.extractOne(self.text, initial_word, scorer = fuzz.ratio)[1] >= 80:
			my_memory = None
		else:
			my_memory = None

		return my_memory

	def get_reply(self):
		print(self.memory_brain())
		
		#clean_text = process.extractOne(self.text, initial_word, scorer = fuzz.ratio)[0]

		if self.memory_brain() == 'Metrics Value':
			#reply_message = Metrics_Doctor(self.text).get_reply_message()
			reply_message = {
					'message_format': 'text',
					'text': 'Hey I know you are asking me about Definition'
			}

		elif self.memory_brain() == 'Metrics Definition':
			#reply_message = Definition_Doctor(self.text).get_reply_message()
			reply_message = {
					'message_format': 'text',
					'text': 'Hey I know you are asking me about Definition'
			}

		elif self.memory_brain() == 'Subscription Setting':
			#reply_message = Subscription_Doctor(self.text).get_reply_message()
			reply_message = {
					'message_format': 'text',
					'text': 'Hey I know you are asking me about Subscription'
			}


		elif self.memory_brain() == None:
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
