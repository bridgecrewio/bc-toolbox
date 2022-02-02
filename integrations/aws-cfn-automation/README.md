This example shows how to integrate Bridgecrew into AWS accounts using CloudFormation, without clicking through the Bridgecrew console for each account.

This approach uses our automated CloudFormation template that accepts a Bridgecrew API key, as well as a Lambda function that you host that generates UUID values. These values get used as the "External ID" for the created roles. The function gets invoked using CloudFormation's "custom resource" mechanism that can invoke external Lambda functions.

The Lambda function is optional, but is the best way to dynamically generate UUID values. You may populate UUID values another way if you wish.

You will need [this](https://bc-cf-template-890234264427-prod.s3.us-west-2.amazonaws.com/read_only_template_api.yml) CloudFormation template to get started.

1. Create a Python Lambda function in the AWS account of your choice. You only need one instance of the function across all accounts. For the function code, use the `lambda_function.py` file in this directory.
2. Modify the CloudFormation template above as follows:

    * Under `Resources`, add the following resource block:

    ```yaml
    ExternalIdResource:       #  <------ This is the block you would add, with the ARN of the Lambda
      Type: 'Custom::GenerateUUID'
      Properties:
        ServiceToken: <ARN FOR THE LAMBDA YOU CREATED ABOVE>
    ```

    * Within the `BridgecrewCWSSACrossAccountAccessRole` resource, modify the `AssumeRolePolicyDocument`'s `Condition` value to be:

    ```yaml
    Condition:
      StringEquals:
        'sts:ExternalId':
          Fn::GetAtt:
            - ExternalIdResource
            - UUID
    ```

    Refer to `sample_template.yaml` for an example.

3. You can now use this template to deploy account integrations in any automated fashion without touching the Bridgecrew console.

**Note:** the CloudFormation custom resource mechanism can only invoke Lambda functions in the same region in which the stack is being deployed. You must deploy the Bridgecrew integration stack in the same region where you deployed the Lambda function. This will not affect Bridgecrew functionality (it can still scan all regions, regardless).

