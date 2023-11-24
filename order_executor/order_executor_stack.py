from os import path

from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_sqs as sqs,
)
from constructs import Construct

class OrderExecutorStack(aws_cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        evaluator_lambda =lambda_.Function(self, "MyFunction",
                                                 runtime=lambda_.Runtime.NODEJS_18_X,
                                                 handler="index.handler",
                                                 code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
                                                 )

        # example resource
        queue = sqs.Queue()
        #     self, "OrderExecutorQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
