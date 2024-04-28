import asyncio
import json
import time
import g4f
import aiofiles

#todo https://gpt4free.io/ проверить срочно!!!

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


    def talk_valid_markdown(self, prompts:str='Привет, ты работаешь?', system_prompt:str='', mess:list=[]) -> str:
            # 'Отвечай, пожалуйста, со способом форматирования текста в html' +
            supp_prompts = 'Я пишу тебе из телеграм, для ответа используй MarkdownV2, чтобы не нарушать правила telegram.'
            messages = [{
                "content": prompts, "role": "user"}] # , {"content": system_prompt, "role": "system"}
            
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
            
            return response #.replace('**', '*').replace('!', '\!').replace('.', '\.')

    async def talk_valid_async(self, prompts:str='Привет, ты работаешь?', system_prompt:str='', mess:list=[]) -> str:
            # 'Отвечай, пожалуйста, со способом форматирования текста в html' +
            supp_prompts = 'Я пишу тебе из телеграм, для ответа используй MarkdownV2, чтобы не нарушать правила telegram.'
            messages = [{
                "content": prompts, "role": "user"}] # , {"content": system_prompt, "role": "system"}
            
            # messages = [
            #     {"role": "assistant", "content": system_prompt},
            #     {"role": "user", "content": prompts},
            # ]
            request = g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=messages,
                stream=True,
                # proxy=self.proxy
            )

            return request
            # socks5://42090:Fvsd45@176.106.53.179:42090
            # http://x265.fxdx.in:15259:winteamubt255156:bj4era3m9f8d
            # G4F_PROXY=http://winteamubt255156:bj4era3m9f8d@x265.fxdx.in:15259
            # response = await g4f.ChatCompletion.create_async(
            #     model=g4f.models.gpt_4,
            #     provider=g4f.Provider.Bing,
            #     messages=messages,
            #     stream=True
            #     # proxy=self.proxy
            # )
            
            # # self.output_talk = response.replace('**', '*')
            # async for chunk in response:
            #     if chunk.choices[0].delta.content:
            #         return chunk.choices[0].delta.content
            # return response #.replace('**', '*').replace('!', '\!').replace('.', '\.')
            
    def take_context(self, id:str='722895694') -> list:
            with open('db/context.json', 'r', encoding='utf-8') as f:
                context = json.load(f)
                messages = context[id]
                print(messages)
                return messages


async def main():
    gpt = Gpt(prompts='Привет, ты работаешь?')
    gpt.take_context('722895694')


if __name__ == '__main__':
    asyncio.run(main())