from aws_cdk import core as cdk, aws_lambda, aws_apigateway

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class ExampleCdkDotnetLambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_code_dir = "sample_function"

        example_function = aws_lambda.Function(
            self,
            "DotNetFunction",
            runtime=aws_lambda.Runtime.DOTNET_CORE_3_1,
            code=aws_lambda.Code.from_asset(
                path=lambda_code_dir,
                bundling=cdk.BundlingOptions(
                    image=cdk.DockerImage.from_registry(
                        image="lambci/lambda:build-dotnetcore3.1"
                    ),
                    user="root",
                    command=[
                        "/var/lang/bin/dotnet",
                        "publish",
                        "-c",
                        "Release",
                        "-o",
                        "/asset-output",
                    ],
                ),
            ),
            handler="HelloWorld::HelloWorld.Function::FunctionHandler",
            memory_size=1024,
            timeout=cdk.Duration.minutes(1),
        )

        aws_apigateway.LambdaRestApi(self, "API", handler=example_function)
