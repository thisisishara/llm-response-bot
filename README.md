# llm-response-bot
A rasa bot that can generate and rephrase responses on the fly using LLMs

## Deploying
To deploy and run the bot, `docker` and `docker-compose` is required.
1. Clone the repository and do `cd llm-response-bot`
2. Make sure to copy the `.env.template` to `.env` and add your open-ai API key under the `OPENAI_COMPLETIONS_API_KEY` key
3. Go to the project root directory and run `docker compose up -d` to run everything
4. Widget should be available @ http://localhost:80

## Talking to the bot
The bot is a demo Pizza Shop bot that can do the following:
- say greet
- show the Pizza Shop menu
- tell about Pizza prices
- tell price for an order
- say welcome
- say goodbye

All the bot responses are generated or rephrased using Open AI GPT-3 `text-davinci-003` completions model.  

In case the rate limit is met (3 requests within a minute last I checked), bot will utter the default rephrase response.
