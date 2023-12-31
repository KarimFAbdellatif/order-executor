# Welcome to your CDK Python project!
After following the initialization process written below by CDK.

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

![img.png](img.png)
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
* A consumer for the SQS error messages with.

#
# Welcome to your CDK Python project!

This is a ~~blank~~ project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation

Enjoy!
