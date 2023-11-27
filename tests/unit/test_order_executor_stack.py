import aws_cdk as core
import aws_cdk.assertions as assertions

from order_executor.order_executor_stack import OrderExecutorStack


# example tests. To run these tests, uncomment this file along with the example
# resource in order_executor/order_executor_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OrderExecutorStack(app, "order-executor")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::Lambda::Function", {"Handler": "app.lambda_handler",
                                                               "Runtime": "python3.11", "FunctionName": "Lambda_a"})
    template.has_resource_properties("AWS::Lambda::Function",
                                     {"Handler": "app.lambda_handler",
                                      "Runtime": "python3.11",
                                      "FunctionName": "Lambda_b"})
    template.has_resource_properties("AWS::Lambda::Function",
                                     {"Handler": "app.lambda_handler",
                                      "Runtime": "python3.11",
                                      "FunctionName": "post_lambda"})
    template.has_resource_properties("AWS::DynamoDB::Table",{
        "TableName": "post_orders_table"
    })
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": "order-output"
    })
    template.has_resource_properties("AWS::Events::Rule", {
        "ScheduleExpression": "cron(0 18 * * ? *)"
    })