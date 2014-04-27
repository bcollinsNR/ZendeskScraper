#!/usr/bin/env python

import requests
from os import environ #reads from ~/.bash_profile for vars
from zendesk import Zendesk
import json

view_ids = {
				37020287 : 'All',
                42702057 : 'Tickets/Ruby',     
                44895823 : 'Tickets/Python',
                42730157 : 'Tickets/PHP',
                46179286 : 'Tickets/Java',
                42730177 : 'Tickets/.Net',
                44896553 : 'Tickets/Node.JS',
                42730237 : 'Tickets/LSM',
                42730227 : 'Tickets/WSM',             
                42771018 : 'Tickets/Mobile',
                42730217 : 'Tickets/Insights',
                44896573 : 'Tickets/Browser',
	        	42771028 : 'Tickets/Platform',
                42730207 : 'Tickets/Other'
}

post_url = "https://platform-api.newrelic.com/platform/v1/metrics"

guid = 'com.NewRelic.ZedScraper'
#update bash_profile on server with this info
zendesk = Zendesk(
                  environ['ZENDESK_URL'],
                  environ['ZENDESK_USERNAME'],
                  environ['ZENDESK_APITOKEN'],
                  use_api_token=True,
                  api_version=2,
                  client_args= {"disable_ssl_certificate_validation": True} )


platform_key = environ['NEW_RELIC_APIKEY']

view_blob = zendesk.count_many_views(ids=view_ids.keys())

counted_views = {}

for view in view_blob['view_counts']:
	metric_name = "Component/test2/%s[Tickets]" % view_ids[view['view_id']]
	total_tickets = view['value']
	data =  {
			   "agent":{
			      "host":"db.zendesk.newrelic_tickets",
			      "pid":1234,
			      "version":"1.0.2"
			   },
			   "components":[
			      {
			         "name":"Support Tickets",
			         "guid":guid,
			         "duration":60,
			         "metrics":{
			            metric_name:{
			               "total":total_tickets,
			               "count":1,
			               "min":total_tickets,
			               "max":total_tickets,
			               "sum_of_squares":total_tickets ^ 2
			            }
			         }
			      }
			    ]
			}

	print requests.post(url=post_url, 
						data=json.dumps(data), 
						headers={'X-License-Key': platform_key, 'Content-Type':'application/json',"Accept":"application/json"}
						)
	#todo: print time