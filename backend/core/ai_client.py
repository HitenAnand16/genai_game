import requests
import json

def query_llm(prompt):
    headers = {
    "Authorization": f"Bearer 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",
    "Content-Type": "application/json"
    }
    payload = {
       "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 50
    }    
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        # Check if the response is valid
        if res.status_code == 200:
            res_data = res.json()
            print(f"Response Data: {json.dumps(res_data, indent=2)}")
            if "choices" in res_data and len(res_data["choices"]) > 0:
                return res_data["choices"][0]["message"]["content"]
            else:
                raise KeyError("'choices' not found in the response")
        else:
            raise Exception(f"API Request Failed with status code {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Error during API request: {str(e)}")
        return "Error in generating AI word"
