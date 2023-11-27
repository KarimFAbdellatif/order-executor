from os import path

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_events as events,
    aws_dynamodb as dynamodb,
    aws_stepfunctions_tasks as tasks,
    aws_stepfunctions as sfn,
    aws_apigateway as apigateway,
    aws_sqs as sqs,
    aws_events_targets as targets,
)
from constructs import Construct

class OrderExecutorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        dynamo_db = dynamodb.Table(self,
                                   'My db',
                                   partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
                                   billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)

        order_results = s3.Bucket(self, 'order-results')

        lambda_a = lambda_.Function(self, "Lambda a",
                                    runtime=lambda_.Runtime.PYTHON_3_11,
                                    handler="app.lambda_handler",
                                    code=lambda_.Code.from_asset(path.join("lambdas/lambda_a/")))

        lambda_b = lambda_.Function(self, "Lambda b",
                                    runtime=lambda_.Runtime.PYTHON_3_11,
                                    handler="app.lambda_handler",
                                    code=lambda_.Code.from_asset(path.join("lambdas/lambda_b/")),
                                    environment={
                                        'LOG_BUCKET': order_results.bucket_name}
                                    )
        order_results.grant_read_write(lambda_b)
        post_lambda = lambda_.Function(self, "Post lambda",
                                       runtime=lambda_.Runtime.PYTHON_3_11,
                                       handler="app.lambda_handler",
                                       code=lambda_.Code.from_asset(path.join("lambdas/post_lambda/")),
                                       environment={
                                           'DYNAMODB_TABLE_NAME': dynamo_db.table_name}
                                       )
        dynamo_db.grant_read_write_data(post_lambda)
        scheduler = events.Rule(self, "ExecuteStateMachine",
                                schedule=events.Schedule.cron(hour="18", minute="0"),
                                #TODO set to true before execution.
                                enabled=False
                                )

        start = tasks.LambdaInvoke(self, "Invoke lambda_a",
                                   lambda_function=lambda_a,
                                   output_path="$.Payload"
                                        )
        ####definition = choice.when(condition1, step1).otherwise(step2).afterwards().next(finish)
        get_status = tasks.LambdaInvoke(self, "Invoke lambda_b",
                                        lambda_function=lambda_b,
                                        )
        fail_notification_que = sqs.Queue(self, "Notifications saved",
                          )
        fail_notification = tasks.SqsSendMessage(
            self, "FailNotificationTask",
            queue=fail_notification_que,
            message_body=sfn.TaskInput.from_json_path_at("$.Cause")  # Adjust as needed
        )


        lambda_a_condition = sfn.Condition.boolean_equals('$.results', True)
        map_lambda_b = sfn.Map(self, 'Lambda Iter',  items_path=sfn.JsonPath.string_at("$.orders"))
        #lambda_b_failed = sfn.Fail(self, "Job failed", cause="Lambda_b returned a fail", error="lambda_b has failed")
        #get_status.add_catch(lambda_b_failed, fail_notification )

        state_machine_definition = start.next(sfn.Choice(self, "Successful lambda_a").when(lambda_a_condition, map_lambda_b.iterator(get_status.add_catch(fail_notification))).otherwise(start))
        state_machine = sfn.StateMachine(self, "State Machine",
                                         definition_body=sfn.DefinitionBody.from_chainable(state_machine_definition))
        scheduler.add_target(targets.SfnStateMachine(state_machine))
        api = apigateway.RestApi(self, "lambda-api")
        integration = apigateway.LambdaIntegration(post_lambda)
        api.root.add_method("POST", integration,
                            method_responses=[{"statusCode": "200"}],
                            )


