index_mapping = {
  "settings" : {
    "index.mapping.ignore_malformed": True
  },
  "mappings": {
    "snowplow_events": {
      "dynamic_date_formats": ["yyyy-MM-dd HH:mm:ss.SSS", "strict_date_optional_time", "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"],
      "dynamic_templates": [
        {
          "fields_as_keywords": {
            "match_pattern": "regex",
            "match": "[a-z_]+id$|^ip[a-z_]+|[a-z_]+fingerprint$|[a-z_]+ipaddress",
            "mapping": {
              "type": "keyword"
            }
          }
        }
      ],
      "properties": {
        "dvce_sent_tstamp": {
          "type": "keyword"
        },
        "dvce_created_tstamp": {
          "type": "keyword"
        }
      }
    }
  }
}