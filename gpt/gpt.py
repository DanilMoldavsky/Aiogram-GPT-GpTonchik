import asyncio
import json
import time
import g4f



#! проверка работоспособных провайдеров
# print([
#     provider.__name__
#     for provider in g4f.Provider.__providers__
#     if provider.working
# ])

class Gpt:
    def __init__(self, prompts='Привет, ты работаешь?', proxy:str | None='socks5://42090:Fvsd45@176.106.53.179:42090'):
        self.prompts = prompts
        self.cnt = 0
        self.conf_prompt = 'Rewrite the following text to make it more sarcastic in russian language:'
        self.output1 = ''
        self.output = []
        self.output_talk = ''
        self.proxy = proxy
    
    def talk_valid(self):
            messages = [{"role": "user", "content": self.prompts}]
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=messages,
                proxy=self.proxy
            )
            
            valid_simbol = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я", ",", " ", "-", "." ]
            
            valid_response = ''.join([c for c in response if c.lower() in valid_simbol])
            self.output_talk = valid_response
            print(self.output_talk)
            
    def talk(self):
            messages = [{"role": "user", "content": self.prompts}]
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=messages,
                proxy=self.proxy
            )

            self.output_talk = response
            print(self.output_talk)
            
    def talk_valid_markdown(self, prompts:str='Привет, ты работаешь?', system_prompt:str='', mess:list=[]) -> str:
            messages = [{"content": prompts, "role": "user"}] # , {"content": system_prompt, "role": "system"}
            
            # messages = [
            #     {"role": "assistant", "content": system_prompt},
            #     {"role": "user", "content": prompts},
            # ]
            
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=messages,
                # proxy=self.proxy
            )
            
            # self.output_talk = response.replace('**', '*')
            
            return response.replace('**', '*')
            
    # def talk(self):
    #         with open('response.json', 'r', encoding="utf-8") as file:
    #             data = json.load(file)
    #         data["content"] *= 6
    #         message = ''.join([c for c in data["content"][:4701]])
    #         print(len(message)) 
    #         # messages = [{"role": "user", "content": data["content"]}]
    #         messages = [{"role": "user", "content": message}]
    #         response = g4f.ChatCompletion.create(
    #             model=g4f.models.gpt_4,
    #             provider=g4f.Provider.Bing,
    #             messages=messages,
    #             proxy=self.proxy
    #         )
            
    #         valid_simbol = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
    #         "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я", ",", " ", "-", "." ]
            
    #         valid_response = ''.join([c for c in response if c.lower() in valid_simbol])
    #         valid_response *= 13
    #         self.output_talk = valid_response
    #         data = {"role": "assistant", "content": self.output_talk, "lenght": len(self.output_talk)}
    #         # data["content"] = data["content"].encode("utf-8").decode("unicode_escape")
    #         file_name = 'response.json'
            
    #         # with open(file_name, 'w', encoding="utf-8") as json_file:
    #         #     json.dump(data, json_file, indent=4, ensure_ascii=False)
                
    #         print(f"Объект JSON успешно записан в файл {file_name}")
    #         print(self.output_talk)

# gpt = GptRewriter(['Привет, ты работаешь?', 'Объясни, 1 градус, больше чем 2', 'Какой цвет похож на синий?', 'Ты работаешь?', ' Ты тут есть?', 'Ты настоящий?'])

