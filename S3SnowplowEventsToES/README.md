# Lambda function for loading Snowplow Events from S3 to ES.

The function is similar to the function for Datadog in the same repository. This function also provides houskeeping for ES.

Two env variables should be set:
1. ES_END_POINT
2. DAYS_TO_KEEP_INDEX
