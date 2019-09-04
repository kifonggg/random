import pandas as pd
from fuzzywuzzy import fuzz, process
import os

class Metrics_Doctor(object):

    def __init__(self, receive_message):

        self.receive_message = receive_message
        self.parameters_mix = pd.read_pickle(os.path.expanduser('parameters_mix.pkl'))
        #self.metrics_database = pd.read_pickle(os.path.expanduser('~/kifong/Chatbot/metrics_data.pkl'))
        self.country_options = ['All Countries', 'Malaysia', 'Philippines', 'Thailand', 'Singapore', 'Vietnam', 'Indonesia', 'Myanmar', 'Cambodia']
        self.dafault_memory = '<Country>, <City>, <Business Group>, <Business Group Breakdown>, <Metrics>, <Date Level>, <Date>'
        self.initial_message = {
                  'message_format': 'quick_reply',
                  'type': ['text']*len(self.country_options),
                  'title': self.country_options,
                  'payload': ['Country: ' + self.country_options[i] for i in range(len(self.country_options))],
                  'text':  "Hi, I know you are asking me about Metrics.\n" +
                            "Please provide me with more details in the following format:\n" + 
                            "<Country>, <City>, <Business Group>, <Business Group Breakdown>, <Metrics>, <Date Level>, <Date>\n"+
                            "Example: Singapore, All cities, Vertical, All Verticals, GMV (USD), Daily, 2019-09-01 \n\n"
                            "You may also follow the options below if you don't know what to input.\n"+
                            "Select a country:"
        }

        self.temp_result_message = {
                  'message_format': 'text',
                    'text': 'Here you are: {}'

        }

        self.json_key = ['Country', 'City', 'Business Group', 'Business Group Breakdown', 'Metrics', 'Date Level', 'Date']



    def execute_sql(self):

        query_frame = '''
        select value
        from datamart.metrics_bank
        where view = '{Date Level}'
        and country = '{Country}'
        and city = '{City}'
        and business_group = '{Business Group}'
        and business_group_breakdown = '{Business Group Breakdown}'
        and metric = '{Metrics}'
        and date_local in ('{Date}')
        '''

        return "The metrics your ask is "




    def ask_for_more_parameter(self,parameter, last_memory, more_count):

        if parameter == 'Date':
            new_message = {
              'message_format': 'text',
              'text': 'You have selected {}\n'.format(last_memory)+
                      'Next, please select a date in YYYY-MM-DD format (Eg. 2019-07-20).'
            }

        else:
            current_memory = {}
            for i in range(len(self.json_key)):
                current_memory[self.json_key[i]] = last_memory.split(',')[i].strip()

            new_mix = self.parameters_mix
            for j in current_memory.keys():
               
                if (current_memory[j].find('<') < 0) or (current_memory[j].find('>') < 0):
                    print(j)
                    print(current_memory[j])
                    new_mix = new_mix[new_mix[j] == current_memory[j]]

            new_options = ['Back'] + sorted(list(new_mix[parameter].unique()))
            print(new_options)


            if len(new_options) >= 12:
                if more_count == 0:
                    new_options = new_options[0:12] + ['More..']
                else:
                    multiplier = more_count-1
                    if len(new_options) >= ((12*multiplier)+13) :
                        new_options = new_options[(12*multiplier) +1: (12*multiplier)+1 + 12] + ['More' + '.'*(more_count+1)]
                    else:
                        new_options = new_options[(12*multiplier) +1: ]

            new_message = {
                  'message_format': 'quick_reply',
                  'type': ['text']*len(new_options),
                  'title': new_options,
                  'payload': [parameter + ': ' + new_options[i] for i in range(len(new_options))],
                  'text': 'You have selected {}\n'.format(last_memory)+
                          'Next, please select a '+parameter.lower()
            }

        return new_message



    def memory_manager(self):
        print('welcome to memory manager')

        try:
            file_r = open('metrics_doctor.txt', 'r')
            memory = file_r.read() 
        except:
            file_= open('metrics_doctor.txt', 'w')
            file_.write(self.dafault_memory)
            file_.close()


        if self.receive_message == 'Metrics Value':
            file_w = open('metrics_doctor.txt', 'w')
            file_w.write(self.dafault_memory)
            file_w.close()

        elif (len(self.receive_message.split(',')) == 7) and ((self.receive_message.find('<') < 0) or (self.receive_message.find('>') < 0)):
            file_w = open('metrics_doctor.txt', 'w')
            file_w.write(self.receive_message)
            file_w.close()

        elif self.receive_message.find('More') > 0:
            new_memory = memory + '|' +self.receive_message
            file_w = open('metrics_doctor.txt', 'w')
            file_w.write(new_memory)
            file_w.close()
        
        elif self.receive_message.find('Back') > 0:
            print('Remove some thing')
            replace_input_from = memory[memory[: memory.find(', <')].rfind(', ')+2 : memory.find(', <')]
            replace_input_to = '<'+self.json_key[self.json_key.index(self.receive_message.split(':')[0].strip())-1]+'>'
            new_memory = memory.replace(replace_input_from, replace_input_to)
            file_w = open('metrics_doctor.txt', 'w')
            file_w.write(new_memory)
            file_w.close()

        else:
            print('Add more thing')
            replace_input_from = '<'+self.receive_message.split(':')[0]+'>'
            replace_input_to = self.receive_message.split(':')[1]
            new_memory = memory.replace(replace_input_from, replace_input_to)
            print(new_memory)
            file_w = open('metrics_doctor.txt', 'w')
            file_w.write(new_memory)
            file_w.close()

        file_r = open('metrics_doctor.txt', 'r')
        memory = file_r.read() 
        return memory



    def get_reply_message(self):

        metrics_doctor_memory = self.memory_manager()
        print(metrics_doctor_memory)
      # If users input the complete command or construted the command
        if (len(metrics_doctor_memory.split(',')) == 7) and ((metrics_doctor_memory.find('<') < 0) or (metrics_doctor_memory.find('>') < 0)):
            parameters = metrics_doctor_memory.split(',')
            parameters_clean = {}
            for i in range(len(parameters)):
                parameters_clean[self.json_key[i]] = parameters[i].strip()
            return {
              'message_format': 'text',
              'text': 'Your had selected {}\n'.format(metrics_doctor_memory) + 
                      'Here is your metrics: {}'.format(100000)
            }#self.execute_sql(parameters_clean)

        elif metrics_doctor_memory.strip() == self.dafault_memory:
            return self.initial_message
            
        else:
            if metrics_doctor_memory.find('More') > 0:
                print('Show More Options')
                count_more_time = metrics_doctor_memory.count('.')
                next_ask = metrics_doctor_memory.split('|')[1].split(':')[0].strip()
                file_w = open('metrics_doctor.txt', 'w')
                file_w.write(metrics_doctor_memory.replace('|City: More','').replace('.',''))
                file_w.close()
                print(next_ask)
                print(count_more_time)
                print(metrics_doctor_memory)
                return self.ask_for_more_parameter(next_ask, metrics_doctor_memory, count_more_time)
            else:
                next_ask = metrics_doctor_memory[metrics_doctor_memory.find('<')+1: metrics_doctor_memory.find('>')]
                count_more_time = metrics_doctor_memory.count('.')
                print(next_ask)
                print(count_more_time)
                print(metrics_doctor_memory)
                return self.ask_for_more_parameter(next_ask, metrics_doctor_memory, count_more_time)



