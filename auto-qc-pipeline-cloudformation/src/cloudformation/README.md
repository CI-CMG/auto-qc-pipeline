# AutoQC Pipeline CloudFormation Deploy

## CLI Setup

### Install the AWS CLI and saml2aws command to log into the CU AWS account
```bash
brew tap versent/homebrew-taps
brew install saml2aws
brew install awscli
```

## Multiple Role Configuration
If you are part of multiple CU AWS accounts, you will need to determine the role for the appropriate account.

First, you will need to set up a general CU AWS profile:
```bash
saml2aws configure -a cu --idp-provider ShibbolethECP --mfa auto --url https://fedauth.colorado.edu/idp/profile/SAML2/SOAP/ECP --profile cu
```

Hit enter past any fields that are pre-populated.  Your credentials will be your CU IdentiKey and password.

Next, run the following to list the accounts you have access to:
```bash
saml2aws list-roles -a cu
```

Note the ARN for the mggdev role.

## Set up AutoQC Pipeline saml2aws profile
If you have multiple roles, run the following, replacing ROLE_ARN with the role noted above:
```bash
saml2aws configure -a mggdev --idp-provider ShibbolethECP --mfa auto --url https://fedauth.colorado.edu/idp/profile/SAML2/SOAP/ECP --profile mggdev --role ROLE_ARN
```
Otherwise run:
```bash
saml2aws configure -a mggdev --idp-provider ShibbolethECP --mfa auto --url https://fedauth.colorado.edu/idp/profile/SAML2/SOAP/ECP --profile mggdev
```
Hit enter past any fields that are pre-populated.  Your credentials will be your CU IdentiKey and password.

Run the following to set up the AWS profile:
```bash
aws configure --profile mggdev
```

You can hit enter to skip past the "AWS Access Key ID" and "AWS Secret Access Key".
For the region use "us-west-2".  For the output format, use "json".

## Using saml2aws and the AWS CLI

Before you can use the AWS CLI, you will need to login using saml2aws.
```bash
saml2aws login -a mggdev
```
Hit enter to skip past the saved username and password.  Choose "Duo Push" to start MFA.

To use the AWS CLI, you will need to use the --profile option.  For example:
```bash
aws --profile mggdev ec2 describe-instances
```

Your login may timeout.  If this happens, just use saml2aws to log in again.

## Default AWS Profile

It is recommended to disable your default AWS profile.  To do this, edit ~/.aws/credentials and 
delete the [default] sections.


## AutoQC Pipeline Stack Deployment
Creation of a deployment stack will only need to be done once per dev user or stack type (prod, test, etc.).
This will create a bucket to store binaries, configuration, and other CloudFormation templates.
Each deployment stack will segregate resources from each other.  A stack prefix
will be used to identify the stack.

### Deploy Deployment Template

Unzip the CloudFormation artifact bundle:
```bash
unzip auto-qc-pipeline-cloudformation-VERSION.zip
``` 

If you are using the AWS console (web page) to set up the stack, select the
auto-qc-pipeline-cloudformation-VERSION/deploy/deployment-stack.yaml file to upload.

Otherwise, if you are using the AWS CLI to deploy, create a file, deployment-parameters.json.  There is a
template at auto-qc-pipeline-cloudformation-VERSION/deploy/deployment-parameters-template.json.  

Run the following to deploy the deployment stack, using an appropriate name for STACK_NAME:
```bash
aws cloudformation create-stack \ 
  --profile mggdev \
  --stack-name STACK_NAME \
  --template-body file://auto-qc-pipeline-cloudformation-VERSION/deploy/deployment-stack.yaml \
  --parameters file://deployment-parameters.json
```


## AutoQC Pipeline Stack

### Deploy A New Stack

Unzip the CloudFormation artifact bundle:
```bash
unzip auto-qc-pipeline-conveyor-cloudformation-VERSION.zip
``` 

Synchronize your artifacts to the deployment area, replace BUCKET_NAME with the deployment bucket:
```bash
aws --profile mggdev s3 sync auto-qc-pipeline-conveyor-cloudformation-VERSION s3://BUCKET_NAME/
```

If you are using the AWS console (web page) to set up the stack, use the following url, replace BUCKET_NAME with the deployment bucket:
```
https://s3.amazonaws.com/BUCKET_NAME/stack/auto-qc-pipeline-stack.yaml
```

Otherwise, if you are using the AWS CLI to deploy, create a file, auto-qc-pipeline-parameters.json.  There is a
template at auto-qc-pipeline-cloudformation-VERSION/stack/auto-qc-pipeline-parameters-template.json. 

Run the following to deploy the stack, using an appropriate name for STACK_NAME, replace BUCKET_NAME with the deployment bucket:
```bash
aws cloudformation create-stack \ 
  --profile mggdev \
  --stack-name STACK_NAME \
  --template-url https://s3.amazonaws.com/BUCKET_NAME/stack/auto-qc-pipeline-stack.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --parameters file://auto-qc-pipeline-parameters.json
```

If you encounter errors, it may be useful to add the --disable-rollback option.  
This will keep the stack on failure and will allow you to see the event log.

### Update Stack
Run the following to update the stack, use the deploy STACK_NAME and replace BUCKET_NAME with the deployment bucket:
```bash
aws cloudformation update-stack \ 
  --profile mggdev \
  --stack-name STACK_NAME \
  --template-url https://s3.amazonaws.com/BUCKET_NAME/stack/auto-qc-pipeline-stack.yaml\
  --parameters file://auto-qc-pipeline-parameters.json
```
