from flask import Flask
import json
import logging
import boto3

logger = Flask(__name__)


@logger.route("/api/response", methods=["GET"])
def response():
    BedrockRuntimeWrapper


@logger.route("/api/prompt", methods=["POST"])
def prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    return prompt
        

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

            # Claude requires you to enclose the prompt as follows:
            prompt_with_preface = "\n\nHuman: You will be acting as a AI plant expert named Plant Pal."\
                            "When I write 'BEGIN DIALOGUE' you will enter this role, and all further input"\
                            "from will be from a user seeking assistance about plants."\
                            "You should maintain a friendly customer service tone."\
                            "Here are some important rules you MUST ADHERE to for the interaction: "\
                            "1. Always stay in character, as Plant Pal, an AI from Plant Pals."\
                            "2. If you are unsure how to respond, say 'Sorry, I didn't understand that. Could you repeat the question?'"\
                            "3. If someone asks something unrelated to plants, say,"\
                            "4. Do NOT make up any facts about plants."\
                            "'Sorry, I am Plant Pal and can only provide information on plants. Do you have a plant question today I can help you with?'" \
                            "Here is an example of how to respond in a standard interaction:" \
                            "**<example>"\
                            "User: Hi, how were you created and what do you do?"\
                            "Plant Pal: Hello! My name is Plant Pal, and I was created by Plant Pals to give plant advice." \
                            "What can I help you with today?"\
                            "</example>**"\
                            "Here is the user's question: <question> " + prompt + " </question>"\
                            "How do you respond to the user's question?"\
                            "Think about your answer first before you respond." \
                            "BEGIN DIALOGUE"
            
            enclosed_prompt = prompt_with_preface + "\n\nAssistant:"

            body = {
                "prompt": enclosed_prompt,
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
            logger.error("Couldn't invoke Anthropic Claude")
            raise

    # snippet-end:[python.example_code.bedrock-runtime.InvokeAnthropicClaude]

    # snippet-start:[python.example_code.bedrock-runtime.InvokeModelWithResponseStream]
    async def invoke_model_with_response_stream(self, prompt):
        """
        Invokes the Anthropic Claude 2 model to run an inference and process the response stream.

        :param prompt: The prompt that you want Claude to complete.
        :return: Inference response from the model.
        """

        try:
            # The different model providers have individual request and response formats.
            # For the format, ranges, and default values for Anthropic Claude, refer to:
            # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html

            # Claude requires you to enclose the prompt as follows:
            prompt_with_preface = "\n\nHuman: You will be acting as a AI plant expert named Plant Pal."\
                            "When I write 'BEGIN DIALOGUE' you will enter this role, and all further input"\
                            "from will be from a user seeking assistance about plants."\
                            "You should maintain a friendly customer service tone."\
                            "Here are some important rules you MUST ADHERE to for the interaction: "\
                            "1. Always stay in character, as Plant Pal, an AI from Plant Pals."\
                            "2. If you are unsure how to respond, say 'Sorry, I didn't understand that. Could you repeat the question?'"\
                            "3. If someone asks something unrelated to plants, say,"\
                            "4. Do NOT make up any facts about plants."\
                            "'Sorry, I am Plant Pal and can only provide information on plants. Do you have a plant question today I can help you with?'" \
                            "Here is an example of how to respond in a standard interaction:" \
                            "**<example>"\
                            "User: Hi, how were you created and what do you do?"\
                            "Plant Pal: Hello! My name is Plant Pal, and I was created by Plant Pals to give plant advice." \
                            "What can I help you with today?"\
                            "</example>**"\
                            "Here is the user's question: <question> " + prompt + " </question>"\
                            "How do you respond to the user's question?"\
                            "Think about your answer first before you respond. Put your response in <response></response> tags." \
                            "BEGIN DIALOGUE"

            enclosed_prompt = prompt_with_preface + "\n\nAssistant:"

            body = {
                "prompt": enclosed_prompt,
                "max_tokens_to_sample": 1024,
                "temperature": 0.5,
                "stop_sequences": ["\n\nHuman:"],
            }

            response = self.bedrock_runtime_client.invoke_model_with_response_stream(
                modelId="anthropic.claude-v2", body=json.dumps(body)
            )

            for event in response.get("body"):
                chunk = json.loads(event["chunk"]["bytes"])["completion"]
                yield chunk

        except ClientError:
            logger.error("Couldn't invoke Anthropic Claude v2")
            raise

    # snippet-end:[python.example_code.bedrock-runtime.InvokeModelWithResponseStream]


def invoke(wrapper, model_id, prompt, style_preset=None):
    print("-" * 88)
    print(f"Invoking: {model_id}")
    print("Prompt: " + prompt)

    try:
        if model_id == "anthropic.claude-v2":
            completion = wrapper.invoke_claude(prompt)
            return("answer: " + completion)

    except ClientError:
        logger.exception("Couldn't invoke model %s", model_id)
        raise


async def invoke_with_response_stream(wrapper, model_id, prompt):
    print("-" * 88)
    print(f"Invoking: {model_id} with response stream")
    print("Prompt: " + prompt)
    print("\nResponse stream:")

    try:
        async for completion in wrapper.invoke_model_with_response_stream(prompt):
            print(completion, end="")

    except ClientError:
        logger.exception("Couldn't invoke model %s", model_id)
        raise

    print()


def usage_demo():
    """
    Demonstrates the invocation of Anthropic Claude 2
    """
    logging.basicConfig(level=logging.INFO)
    print("-" * 88)
    print("Welcome to the Amazon Bedrock Runtime demo.")
    print("-" * 88)

    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
    
    wrapper = BedrockRuntimeWrapper(client)

    while True:
        try:
            user_input = input("User: ")
            if user_input == "exit":
                break
        except KeyboardInterrupt:
            break
        invoke(wrapper, "anthropic.claude-v2", user_input)

if __name__ == "__main__":
    usage_demo()
# snippet-end:[python.example_code.bedrock-runtime.BedrockRuntimeWrapper.class]