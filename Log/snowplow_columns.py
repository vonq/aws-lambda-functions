snowplow_columns = [
  # The application (site, game, app etc) this event belongs to, and the tracker platform
  "app_id",
  "platform",

  # Date/time
  "etl_tstamp",
  "collector_tstamp",
  "dvce_created_tstamp",

  # Transaction (i.e. this logging event)
  "event",
  "event_id",
  "txn_id",

  # Versioning
  "name_tracker",
  "v_tracker",
  "v_collector",
  "v_etl",

  # User and visit
  "user_id",
  "user_ipaddress",
  "user_fingerprint",
  "domain_userid",
  "domain_sessionidx",
  "network_userid",

  # Location
  "geo_country",
  "geo_region",
  "geo_city",
  "geo_zipcode",
  "geo_latitude",
  "geo_longitude",
  "geo_region_name",

  # Other IP lookups
  "ip_isp",
  "ip_organization",
  "ip_domain",
  "ip_netspeed",

  # Page
  "page_url",
  "page_title",
  "page_referrer",

  # Page URL components
  "page_urlscheme",
  "page_urlhost",
  "page_urlport",
  "page_urlpath",
  "page_urlquery",
  "page_urlfragment",

  # Referrer URL components
  "refr_urlscheme",
  "refr_urlhost",
  "refr_urlport",
  "refr_urlpath",
  "refr_urlquery",
  "refr_urlfragment",

  # Referrer details
  "refr_medium",
  "refr_source",
  "refr_term",

  # Marketing
  "mkt_medium",
  "mkt_source",
  "mkt_term",
  "mkt_content",
  "mkt_campaign",

  # Custom Contexts
  "contexts",

  # Structured Event
  "se_category",
  "se_action",
  "se_label",
  "se_property",
  "se_value", # Technically should be a Double but may be rendered incorrectly by Cascading with scientific notification (which Redshift can't process)

  # Unstructured Event
  "unstruct_event",

  # Ecommerce transaction (from querystring)
  "tr_orderid",
  "tr_affiliation",
  "tr_total",
  "tr_tax",
  "tr_shipping",
  "tr_city",
  "tr_state",
  "tr_country",

  # Ecommerce transaction item (from querystring)
  "ti_orderid",
  "ti_sku",
  "ti_name",
  "ti_category",
  "ti_price",
  "ti_quantity",

  # Page Pings
  "pp_xoffset_min",
  "pp_xoffset_max",
  "pp_yoffset_min",
  "pp_yoffset_max",

  # User Agent
  "useragent",

  # Browser (from user-agent)
  "br_name",
  "br_family",
  "br_version",
  "br_type",
  "br_renderengine",

  # Browser (from querystring)
  "br_lang",
  # Individual feature fields for non-Hive targets (e.g. Infobright)
  "br_features_pdf",
  "br_features_flash",
  "br_features_java",
  "br_features_director",
  "br_features_quicktime",
  "br_features_realplayer",
  "br_features_windowsmedia",
  "br_features_gears",
  "br_features_silverlight",
  "br_cookies",
  "br_colordepth",
  "br_viewwidth",
  "br_viewheight",

  # OS (from user-agent)
  "os_name",
  "os_family",
  "os_manufacturer",
  "os_timezone",

  # Device/Hardware (from user-agent)
  "dvce_type",
  "dvce_ismobile",

  # Device (from querystring)
  "dvce_screenwidth",
  "dvce_screenheight",

  # Document
  "doc_charset",
  "doc_width",
  "doc_height",

  # Currency
  "tr_currency",
  "tr_total_base",
  "tr_tax_base",
  "tr_shipping_base",
  "ti_currency",
  "ti_price_base",
  "base_currency",

  # Geolocation
  "geo_timezone",

  # Click ID
  "mkt_clickid",
  "mkt_network",

  # ETL tags
  "etl_tags",

  # Time event was sent
  "dvce_sent_tstamp",

  # Referer
  "refr_domain_userid",
  "refr_dvce_tstamp",

  # Derived contexts
  "derived_contexts",

  # Session ID
  "domain_sessionid",

  # Derived timestamp
  "derived_tstamp",

  # Derived event vendor/name/format/version
  "event_vendor",
  "event_name",
  "event_format",
  "event_version",

  # Event fingerprint
  "event_fingerprint",

  # True timestamp
  "true_tstamp",

  # Fields modified in PII enrichemnt (JSON String)
  # "pii" either this column or true_tstamp doesn't exist in our data
]
