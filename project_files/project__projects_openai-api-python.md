OpenAI API in Python
intermediate

OpenAI API in Python
====================

Call OpenAI models directly from Python, beyond the ChatGPT interface.

Start building, submit solution and get feedback from the community.

Start Working
### Project Description

In this project, you will stop using ChatGPT through the browser and start calling OpenAI models directly from Python. The [OpenAI API](https://developers.openai.com/api/reference/python) gives you control over things the chat interface does not, like customizing the system message, adjusting temperature, setting token limits, and integrating LLM responses into your own code.

### Project Requirements

* Create an OpenAI account and get an API key
* Install `openai` and store the key as an environment variable
* Set up the client using the current syntax:

python

```
  from openai import OpenAI  client = OpenAI()
```

* Make your first API call using `client.chat.completions.create()`
* Experiment with the following parameters:

  + `temperature` — controls randomness
  + `max_tokens` — limits response length
  + `system` message — sets the model's behavior
* Build a small script that takes user input and returns a model response
* Compare outputs at different temperature values

### Technologies to Use

* Python
* openai >= 1.0.0
* python-dotenv
* Jupyter Notebook or any Python IDE

### What You Will Learn

You will understand how to interact with LLMs programmatically, what tokens are, and how parameters like temperature change model behavior. This is the foundation for every LLM project that follows.

### Want to See a Solution?

A full walkthrough of this project is available on Towards Data Science: 🔗 [Cracking Open the OpenAI Python API.](https://towardsdatascience.com/cracking-open-the-openai-python-api-230e4cae7971/?utm_source=roadmap&utm_medium=Referral&utm_campaign=TDS+roadmap+integration)

> Note: The article was written in 2023 and uses the legacy OpenAI Python client syntax (`openai.ChatCompletion.create()`), which was deprecated in late 2023. The concepts are still valid, but make sure to use the updated client syntax shown above.

