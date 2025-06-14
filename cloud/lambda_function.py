import json
import urllib.request
import concurrent.futures
import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def fetch_url(url, timeout=10):
    """Fetch content from a URL."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return {"url": url, "status": conn.getcode(), "length": len(conn.read())}
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}

def lambda_handler(event, context):
    """Lambda handler to process SQS messages in parallel."""
    logger.info(f"Received {len(event['Records'])} SQS messages")
    
    # Initialize SQS client
    sqs = boto3.client('sqs')
    queue_url = "https://sqs.us-east-1.amazonaws.com/357063408379/ParallelTaskQueue"

    # Extract URLs and receipt handles from SQS messages
    urls = []
    receipt_handles = []
    for record in event['Records']:
        body = json.loads(record['body'])
        urls.append(body['url'])
        receipt_handles.append(record['receiptHandle'])

    # Process URLs in parallel using ThreadPoolExecutor
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            results.append(future.result())

    # Delete processed messages from SQS
    for receipt_handle in receipt_handles:
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        logger.info(f"Deleted message with receipt handle: {receipt_handle}")

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }