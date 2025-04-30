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
