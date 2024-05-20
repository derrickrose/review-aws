import json
import logging

logger = logging.getLogger("lambda_factorial_test_logs_metrics")

"""
Aws Lambda PowerTools Python 

https://docs.powertools.aws.dev/lambda/python/latest/tutorial/
"""


def factorial(number: int) -> int:
    fact = 1
    for i in range(1, number + 1):
        fact *= i
    return fact


def lambda_handler(event, context):
    if len(logging.getLogger().handlers) > 0:
        # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
        # `.basicConfig` does not execute. Thus we set the level directly.
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
    logger.info(msg=f"calculate the factorial of {event['input']}")
    fact = factorial(event['input'])
    logger.info(msg=f'Factorial calculated of {event["input"]} is {fact}')
    return {
        'statusCode': 200,
        'body': json.dumps({"input": event["input"], "factorial": fact})
    }


if __name__ == '__main__':
    print("&")
    event = {'input': 6}
    lambda_handler(event, None)
    print("b")
