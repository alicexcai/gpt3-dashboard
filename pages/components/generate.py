import openai
import itertools
import pandas as pd

def generate(params, db, cursor, apikey):
    
    openai.api_key = apikey
    
    prompt_id = params.prompt_id
    prompt = params.prompt
    model = params.model
    temp = params.temp
    max_tokens = params.max_tokens
    top_p = params.top_p
    frequency_penalty = params.freq_penalty
    presence_penalty = params.pres_penalty
    num_output = params.num_output
    stop = params.stop_sequences
    
    full_response = []
    parsed_response = pd.DataFrame(columns=['model', 'completion', 'finish_reason', 'temperature', 'max_tokens', 'other_parameters'])
    
    for model, temp in itertools.product(model, temp):

        response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=num_output,
        stop=stop,
        )
        
        other_parameters = {
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'stop': stop,
        }
    
        for i in range(num_output):
            completion_data = [prompt_id, model, response['choices'][i]['text'], response['choices'][i]['finish_reason'], temp, max_tokens, str(other_parameters)]
            parsed_response.loc[len(parsed_response)] = completion_data[1:]
            
            cursor.execute(
            """
            INSERT INTO completions ( prompt_id, model, completion, finish_reason, temperature, max_tokens, other_parameters )
            VALUES( ?, ?, ?, ?, ?, ?, ? )
            """, completion_data )
            db.commit()
        full_response.append(response)
        
    return full_response, parsed_response