import json
import logging
import uuid
from urllib.request import build_opener, HTTPHandler, Request

logger = logging.getLogger()
logger.setLevel('DEBUG')


def lambda_handler(event, context):
    message = "Message failed to parse"
    logger.info('REQUEST RECEIVED:\n %s', json.dumps(event))
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        if isinstance(message, str):
            message = json.loads(message)

        uuid_str = str(uuid.uuid4())

        send_response(message, context, 'SUCCESS', {"UUID": uuid_str})

    except Exception as e:
        logger.error('FAILED!')
        logger.error(e, exc_info=True)
        send_response(message, context, "FAILED", {"Message": str(e)})
        raise e


def send_response(message, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": message.get('StackId', ''),
        "RequestId": message['RequestId'],
        "LogicalResourceId": message['LogicalResourceId'],
        "Data": response_data
    })

    logger.info('ResponseURL: %s', message['ResponseURL'])
    logger.info('ResponseBody: %s', response_body)

    opener = build_opener(HTTPHandler)
    response_body_encode = response_body.encode()
    request = Request(message['ResponseURL'], data=response_body_encode)
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', str(len(response_body_encode)))
    request.get_method = lambda: 'PUT'
    response = opener.open(request)
    logger.info("Status code: %s", response.getcode())
    logger.info("Status message: %s", response.msg)