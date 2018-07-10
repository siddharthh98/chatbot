#Input Adapter http://chatterbot.readthedocs.io/en/stable/input/create-an-input-adapter.html
#Output Adapter http://chatterbot.readthedocs.io/en/stable/output/create-an-output-adapter.html
#Storage Adapter http://chatterbot.readthedocs.io/en/stable/storage/create-a-storage-adapter.html
#Comparsion logic http://chatterbot.readthedocs.io/en/stable/comparisons.html
#Specific Response Adapter 

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import csv

with open('testfile.csv') as csvfile:
  logic_adapters = [
        {
              "import_path": "chatterbot.logic.BestMatch",
              "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
              "response_selection_method": "chatterbot.response_selection.get_first_response"
        },
        {
          'import_path': 'chatterbot.logic.LowConfidenceAdapter',
          'threshold':0.7,
          'default_response': 'Bot is unable to give answer for this question. Local guide will help you out now.'
        }
      ]

  filters = [
        "chatterbot.filters.RepetitiveResponseFilter"
      ]

  preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
      ]

  chatbot = ChatBot(
      name='Expedia Bot',
      logic_adapters=logic_adapters,    
      input_adapter='chatterbot.input.TerminalAdapter',
      output_adapter='chatterbot.output.TerminalAdapter',
      filters=filters,
      preprocessors=preprocessors
  )

  chatbot.set_trainer(ListTrainer)
  conversations = csv.reader(csvfile, delimiter=',')
  for conversation in conversations:
    this_conversations = []
    this_conversations.append(conversation[0])
    this_conversations.append(conversation[1])
    chatbot.train(this_conversations)

  while True:
      try:
          response = chatbot.get_response(None)

      except (KeyboardInterrupt, EOFError, SystemExit):
          break