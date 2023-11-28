# Welcome to your CDK Python project!
To deploy this code locally: 
Export the AWS environment Variables and run;

```
$ cdk diff
```
If there are no errors:

```
$ cdk deploy 
```


# To have automatic gitlab deployment:

## Set up your configuration data belonging to the desired AWS account - [Dev];
### Auto-deploy - *Short term credentials* would need to be updated before push.
Any push to branch will trigger the test-cdk-template.yml which would return an error if there is incorrect template.

Any push to Main branch would result in a cdk automatic CDK diff -> CDK deploy if no errors are triggered.

  * Secrets;
    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY
    * AWS_SESSION_TOKEN
  * Variables
    * CDK_DEFAULT_ACCOUNT
    * CDK_DEFAULT_REGION

## The cdk stack is divided into two parts: 
* Post Lambda 
  * API-Gateway that introduce the POST method to call the Lambda function
  * DynamoDB database - No actual insertion done to the DB, but the rights are set up.
  * The lambda function generation
* State machine triggered by a scheduler, the state machine contains: 
  * Lambda a 
  * Choice to loop through Lambda a until randomization provides a true statement.
  * Lambda b 
  * SQS to queue up a message when lambda b throws an error. The message can then be consumed by a Slack notification app, webhook notification or otherwise.

## Testing
* Components of the template are tested to insure that they exist and have the proper properties.
* Testing occurs everytime any branch is pushed.

### Improvements for security and development:
* Introduce a config setup that would enable deployments to multiple environments.
* Set up an AWS user that would have long-term credential access to the desired accounts which would mean less secrets' update required.
* More complex testing of the stack depending on the requirements. 
* A consumer for the SQS error messages with .
