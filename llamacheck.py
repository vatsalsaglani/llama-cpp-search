# ignore this is just a test file..
from llama_cpp import Llama

llm = Llama(
    model_path="./model/Phi-3-mini-4k-instruct-q4.gguf",
    n_gpu_layers=-1,  # Uncomment to use GPU acceleration
    seed=1337,  # Uncomment to set a specific seed
    n_ctx=4096,  # Uncomment to increase the context window
    n_threads=16)

input_text = """<|system|>
You are a helpful assistant with access to the following functions:

{'name': 'fetchName',
 'description': 'fetch the name and password from message',
 'parameters': {'properties': {'username': {'title': 'Username',
    'type': 'string'},
   'password': {'title': 'Password', 'type': 'string'}},
  'required': ['username', 'password'],
  'title': 'FetchName',
  'type': 'object'}}

To use a function respond with:

<singlefunction>
    <functioncall> {{fn}} </functioncall>
</singlefunction>

Edge cases you must handle:
- If there are no functions that match the user request, you will respond politely that you cannot help.
- Just provide the function call output and nothing else. End you response once you provide the function call.
- Don't provide any text after the `</singlefunction>` token.

Refer the below provided output example for function calling
Question: What's the weather in NY?
<singlefunction>
    <functioncall> {"name": "getWeather", "parameters": {"city": "NY"}} </functioncall>
</singlefunction>
</functioncallend>
<|end|>
<|user|>
My username is vatsals and password is Password123@11<|end|>
<|assistant|>
"""

output = llm(
    input_text,  # Prompt
    max_tokens=
    256,  # Generate up to 32 tokens, set to None to generate up to the end of the context window
    echo=False,  # Echo the prompt back in the output
    # stream=True,
    stop=["</singlefunction>"])

print(output)
# for op in output:
#     print(op.get("choices")[0].get("text"), flush=True, end="")
# print('\n')
# print(type(op))
# print('\n\n')
# print(output)
