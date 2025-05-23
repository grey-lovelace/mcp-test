
import boto3
from langchain_aws import ChatBedrockConverse

aws_profile_name = "dev"
aws_region = "us-east-1"
boto3.setup_default_session(profile_name=aws_profile_name)
BEDROCK_CLIENT = boto3.client("bedrock-runtime", aws_region)
llm = ChatBedrockConverse(
    client=BEDROCK_CLIENT,
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",
    max_tokens=1000,
    temperature=0.2,
    top_p=0.9,
)

# from phoenix.otel import register
# tracer_provider = register(auto_instrument=True, endpoint="http://localhost:6006/v1/traces", project_name="default")