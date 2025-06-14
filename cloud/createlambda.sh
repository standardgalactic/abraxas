aws lambda create-function \
  --function-name ParallelTaskProcessor \
  --zip-file fileb://lambda_function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.9 \
  --role arn:aws:iam::357063408379:role/LambdaParallelRole \
  --timeout 30 \
  --memory-size 256
