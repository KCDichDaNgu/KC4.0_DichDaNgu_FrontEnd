from itertools import groupby
import re
import aiofiles
import json

async def save_dialogue_group_by_speaker(data, path):
    dialogue = []
    try:
        an_iterator = groupby(data, lambda x: x["alternatives"][0]["speaker"])   

        for key, group in an_iterator:
            content = ""
            start_time = 9999
            end_time = 0

            for word in group:
                start_time = min(start_time, word["start_time"])
                end_time = max(start_time, word["end_time"])
                content += word["alternatives"][0]["content"] + " "

            content = re.sub(r'\s([?.!",](?:\s|$))', r"\1", content)

            speech = dict(user=key, content=content, start_time=start_time, end_time=end_time)
            dialogue.append(speech)

    except Exception as e:
        content = ""
        start_time = 9999
        end_time = 0

        for word in data:
            start_time = min(start_time, word["start_time"])
            end_time = max(start_time, word["end_time"])
            content += word["alternatives"][0]["content"] + " "

        content = re.sub(r'\s([?.!",](?:\s|$))', r"\1", content)

        speech = dict(user='default', content=content, start_time=start_time, end_time=end_time)
        dialogue.append(speech)

    async with aiofiles.open(path, 'w+') as f:

        await f.write(json.dumps(dialogue))

        await f.close()
    
    return dialogue

async def save_txt_dialogue_from_json(dialogue, path):
    
    async with aiofiles.open(path, 'w+') as f:
        
        if len(dialogue) == 1: 
            line = dialogue[0]
            
            new_line = line['content']            
            await f.write(new_line)
            
        else:
            for line in dialogue:
                new_line = 'User {user} ({start_time}s - {end_time}s): {content}\n'.format(user=line['user'], start_time=line['start_time'], end_time=line['end_time'], content=line['content'])
                
                await f.write(new_line)
        
        f.close()   