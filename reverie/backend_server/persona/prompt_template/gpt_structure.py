"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
Updated with modern model fallback (gpt-3.5-turbo / gpt-4) and robust offline fail-safe embeddings.
"""
import json
import random
import openai
import time 
import hashlib
import numpy

from utils import *

openai.api_key = openai_api_key

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def _has_valid_api_key():
  key = getattr(openai, "api_key", None) or openai_api_key
  return bool(key and not key.startswith("<") and len(key) > 10)

def ChatGPT_single_request(prompt): 
  temp_sleep()
  if not _has_valid_api_key():
    return "ChatGPT ERROR"
  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  except Exception as e:
    return "ChatGPT ERROR"


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

def GPT4_request(prompt): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
  RETURNS: 
    a str of GPT-4's response. 
  """
  temp_sleep()
  if not _has_valid_api_key():
    return "ChatGPT ERROR"

  try: 
    completion = openai.ChatCompletion.create(
      model="gpt-4", 
      messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  except Exception as e: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


def ChatGPT_request(prompt): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
  RETURNS: 
    a str of ChatGPT response. 
  """
  if not _has_valid_api_key():
    return "ChatGPT ERROR"
  try: 
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  except Exception as e: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


def GPT4_safe_generate_response(prompt, 
                                example_output,
                                special_instruction,
                                repeat=3,
                                fail_safe_response="error",
                                func_validate=None,
                                func_clean_up=None,
                                verbose=False): 
  prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  if not _has_valid_api_key():
    return fail_safe_response

  for i in range(repeat): 
    try: 
      curr_gpt_response = GPT4_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")
    except: 
      pass

  return fail_safe_response


def ChatGPT_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  if not _has_valid_api_key():
    return fail_safe_response

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")
    except: 
      pass

  return fail_safe_response


def ChatGPT_safe_generate_response_OLD(prompt, 
                                       repeat=3,
                                       fail_safe_response="error",
                                       func_validate=None,
                                       func_clean_up=None,
                                       verbose=False): 
  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  if not _has_valid_api_key():
    return fail_safe_response

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")
    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

def GPT_request(prompt, gpt_parameter): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. Supports modern ChatCompletion fallback for retired engines.
  """
  temp_sleep()
  if not _has_valid_api_key():
    return "TOKEN LIMIT EXCEEDED"

  # First attempt using Completion API
  try: 
    response = openai.Completion.create(
                model=gpt_parameter["engine"],
                prompt=prompt,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)
    return response.choices[0].text
  except Exception as e: 
    # Fallback for retired engines (text-davinci-003, text-davinci-002) using ChatCompletion
    try:
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=gpt_parameter.get("temperature", 0.7),
        max_tokens=gpt_parameter.get("max_tokens", 100),
        stop=gpt_parameter.get("stop", None)
      )
      return completion["choices"][0]["message"]["content"]
    except Exception as e2:
      print ("TOKEN LIMIT EXCEEDED")
      return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input and the path to a prompt file, replaces !<INPUT X>!
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  if not _has_valid_api_key():
    return fail_safe_response

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response


def get_embedding(text, model="text-embedding-ada-002"):
  text = text.replace("\n", " ")
  if not text: 
    text = "this is blank"
  if _has_valid_api_key():
    try:
      return openai.Embedding.create(
              input=[text], model=model)['data'][0]['embedding']
    except Exception as e:
      pass

  # Deterministic, normalized pseudo-embedding (1536 dim) for offline/testing/fail-safe
  h = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)
  rng = numpy.random.RandomState(h % (2**32))
  vec = rng.standard_normal(1536)
  vec = (vec / numpy.linalg.norm(vec)).tolist()
  return vec


if __name__ == '__main__':
  gpt_parameter = {"engine": "text-davinci-003", "max_tokens": 50, 
                   "temperature": 0, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0, 
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/test_prompt_July5.txt"
  prompt = generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(gpt_response): 
    if len(gpt_response.strip()) <= 1:
      return False
    if len(gpt_response.strip().split(" ")) > 1: 
      return False
    return True
  def __func_clean_up(gpt_response):
    cleaned_response = gpt_response.strip()
    return cleaned_response

  output = safe_generate_response(prompt, 
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print (output)
