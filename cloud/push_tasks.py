import boto3
import json

def push_urls_to_sqs(queue_url, urls):
    """Push URLs to SQS queue."""
    sqs = boto3.client('sqs')
    for url in urls:
        message = {'url': url}
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        print(f"Pushed {url} to SQS")

if __name__ == "__main__":
    queue_url = "https://sqs.us-east-1.amazonaws.com/357063408379/ParallelTaskQueue"
    sample_urls = [
        "http://www.example.com",
        "http://www.python.org",
        "http://www.amazon.com",
        "http://www.github.com",
        "http://www.stackoverflow.com"
    ]
    push_urls_to_sqs(queue_url, sample_urls)
