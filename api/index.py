from flask import Flask, request
import json
import logging
import boto3

logger = Flask(__name__)

@logger.route("/api/response", methods=["GET"])
def response():
    prompt = request.args.get('prompt', '') 
    # create a bedrock bedrock_runtime_client
    client =  boto3.client(service_name="bedrock-runtime")
    wrapper = BedrockRuntimeWrapper(client)
    return wrapper.invoke_claude(prompt)

# 

# @app.route("/api/healthchecker", methods=["GET"])
# def healthchecker():
#     return {"status": "success", "message": "Integrate Flask Framework with Next.js"}

# if __name__ == "__main__":
#     app.run()


# logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.bedrock-runtime.BedrockRuntimeWrapper.class]
# snippet-start:[python.example_code.bedrock-runtime.BedrockRuntimeWrapper.decl]
class BedrockRuntimeWrapper:
    """Encapsulates Amazon Bedrock Runtime actions."""

    def __init__(self, bedrock_runtime_client):
        """
        :param bedrock_runtime_client: A low-level client representing Amazon Bedrock Runtime.
                                       Describes the API operations for running inference using
                                       Bedrock models.
        """
        self.bedrock_runtime_client = bedrock_runtime_client
    # snippet-end:[python.example_code.bedrock-runtime.BedrockRuntimeWrapper.decl]

    # snippet-start:[python.example_code.bedrock-runtime.InvokeAnthropicClaude]
    def invoke_claude(self, prompt):
        """
        Invokes the Anthropic Claude 2 model to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Claude to complete.
        :return: Inference response from the model.
        """

        try:
            # The different model providers have individual request and response formats.
            # For the format, ranges, and default values for Anthropic Claude, refer to:
            # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html

            # Prefacing each user prompt with our case specific scenario: an AI plant expert.
            prompt_with_preface = "\n\nHuman: You will be acting as a AI plant expert named Plant Pal."\
                            "When I write 'BEGIN DIALOGUE' you will enter this role, and all further input"\
                            "from will be from a user seeking assistance about plants."\
                            "You should maintain a friendly customer service tone."\
                            "Here are some important rules you MUST ADHERE to for the interaction: "\
                            "1. Always stay in character, as Plant Pal, an AI from Plant Pals."\
                            "2. If you are unsure how to respond, say 'Sorry, I didn't understand that. Could you repeat the question?'"\
                            "3. If someone asks something unrelated to plants, say,"\
                            "4. Do NOT make up any facts about plants."\
                            "5. The response should be no more than 300 characters long."\
                            "'Sorry, I am Plant Pal and can only provide information on plants. Do you have a plant question today I can help you with?'" \
                            "Here is an example of how to respond in a standard interaction:" \
                            "**<example>"\
                            "User: Hi, how were you created and what do you do?"\
                            "Plant Pal: Hello! My name is Plant Pal, and I was created by Plant Pals to give plant advice." \
                            "What can I help you with today?"\
                            "</example>**"\
                            "Here is the user's question: <question> " + prompt + " </question>"\
                            "How do you respond to the user's question?"\
                            "Think about your answer first before you respond."\
                            "BEGIN DIALOGUE"\
                            "\n\nAssistant:"

            body = {
                "prompt": prompt_with_preface,
                "max_tokens_to_sample": 200,
                "temperature": 0.5,
                "stop_sequences": ["\n\nHuman:"],
            }

            response = self.bedrock_runtime_client.invoke_model(
                modelId="anthropic.claude-v2", body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            completion = response_body["completion"]

            return completion

        except ClientError:
            logger.error("Anthropic Claude is having some trouble answering your prompt. Let's try that again.")
            raise
    # snippet-end:[python.example_code.bedrock-runtime.InvokeAnthropicClaude]

def invoke(wrapper, model_id, prompt, style_preset=None):
    print("-" * 88)
    print(f"Your AI Assistant Today: {model_id}")
    print("Prompt: " + prompt)

    try:
        if model_id == "anthropic.claude-v2":
            completion = wrapper.invoke_claude(prompt)
            print("Completion: " + completion)

    except ClientError:
        logger.exception("Hmmm... looks like %s", model_id, " is having some trouble. Try again later!")
        raise

def main_ui():
    """
    Demonstrates the invocation of Anthropic Claude 2
    """
    logging.basicConfig(level=logging.INFO)
    print("-" * 88)
    print("Hello! This is Plant Pal. Nice to meet you!")
    print("-" * 88)

    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
    
    wrapper = BedrockRuntimeWrapper(client)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break
        except KeyboardInterrupt:
            break
        invoke(wrapper, "anthropic.claude-v2", user_input)

# Calls the main class, BedrockRuntimeWrapper, and initiates the program
if __name__ == "__main__":
    main_ui()