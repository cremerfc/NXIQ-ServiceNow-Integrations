#This script will add Success Metrics for the current year to include metrics up to 'last week'
from datetime import *
import requests
import json

#Let's get the current year and week - These will be needed to query IQ server for success metrics
#start by figuring out today
today = datetime.today()
cur_year = today.strftime("%Y")
cur_week = int(today.strftime("%U"))

#Let's define some variables for connecting to IQ Server
iq_user = 'admin'
iq_password = 'password'
iq_url = 'http://localhost:8070/api/v2/reports/metrics'

sn_user = 'admin'
sn_pwd = 'S0n@type'

#Now we need to loop for each week
for counter in range(1,cur_week):
    #set the time period
    time_period = cur_year + '-W' + str(counter)
    r_body = '{"timePeriod": "WEEK","firstTimePeriod": "'+ time_period + '","lastTimePeriod": "' + time_period + '"}'
    #print r_body
    resp = requests.post(iq_url, auth=(iq_user, iq_password) ,data=r_body, headers={'Content-Type':'application/json', 'Accept':'application/json'})
    #print resp.content
    for iq_app in resp.json():
        #for each application we need to submit records to SNOW
        #We want to set relationship to the app and org tables set in SNOW
        #We are going to use the ORG ID and APP ID in the current metric record, we are going to use that value to query SNOW for a matching record 
        date_start = str(iq_app['aggregations'][0]['timePeriodStart'])
        iq_org_id = iq_app['organizationId']
        sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_iq_organization?sysparm_query=organizationid%3D'+ iq_org_id +'&sysparm_fields=sys_id&sysparm_limit=1'
        sn_headers = {"Content-Type":"application/json"}
        sn_resp = requests.get(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers)
        sn_resp_json = sn_resp.json()
        #we need the sys_id (SN internal ID of record) to set the relationship between application and organization
        sn_sys_id_org = sn_resp_json["result"][0]["sys_id"]

        iq_app_id = iq_app['applicationId']
        sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_iq_application?sysparm_query=applicationid%3D'+ iq_app_id +'&sysparm_fields=sys_id&sysparm_limit=1'
        sn_headers = {"Content-Type":"application/json"}
        sn_resp = requests.get(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers)
        sn_resp_json = sn_resp.json()
        #we need the sys_id (SN internal ID of record) to set the relationship between application and organization
        sn_sys_id_app = sn_resp_json["result"][0]["sys_id"]

        #print sn_sys_id_app
        #print sn_sys_id_org


        #data="{\"iq_application\":\"440bb040db91230012552bfa4b961925\",\"iq_organization\":\"2156e444db51230012552bfa4b9619fc\",\"metric\":\"0\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\"2018-08-11\"}"

        #let's add some records to SN!
        #first, reset the sn_url
        sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_success_metric'

        #discoveredCounts SECURITY LOW

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['SECURITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
        
        #discoveredCounts SECURITY MODERATE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['SECURITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
        
        #discoveredCounts SECURITY SEVERE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['SECURITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
        
        #discoveredCounts SECURITY CRITICAL

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['SECURITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts LICENSE LOW

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['LICENSE']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
 
        #discoveredCounts LICENSE MODERATE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['LICENSE']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts LICENSE SEVERE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts LICENSE CRITICAL

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['LICENSE']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
					
        #discoveredCounts QUALITY LOW

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['QUALITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts QUALITY MODERATE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['QUALITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts QUALITY SEVERE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['QUALITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts QUALITY CRITICAL

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['QUALITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #discoveredCounts OTHER LOW

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['OTHER']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #discoveredCounts OTHER MODERATE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['OTHER']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #discoveredCounts OTHER SEVERE

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #discoveredCounts OTHER CRITICAL

        metric = str(iq_app['aggregations'][0]['discoveredCounts']['OTHER']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"discoveredCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #fixedCounts

        #fixedCounts SECURITY LOW

        metric = str(iq_app['aggregations'][0]['fixedCounts']['SECURITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #fixedCounts SECURITY MODERATE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['SECURITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Medium\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #fixedCounts SECURITY SEVERE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['SECURITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #fixedCounts SECURITY CRITICAL

        metric = str(iq_app['aggregations'][0]['fixedCounts']['SECURITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts LICENSE LOW

        metric = str(iq_app['aggregations'][0]['fixedCounts']['LICENSE']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts LICENSE MODERATE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['LICENSE']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts LICENSE SEVERE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #fixedCounts LICENSE CRITICAL

        metric = str(iq_app['aggregations'][0]['fixedCounts']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

					
        #fixedCounts QUALITY LOW

        metric = str(iq_app['aggregations'][0]['fixedCounts']['QUALITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts QUALITY MODERATE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['QUALITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts QUALITY SEVERE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['QUALITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts QUALITY CRITICAL

        metric = str(iq_app['aggregations'][0]['fixedCounts']['QUALITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts OTHER LOW

        metric = str(iq_app['aggregations'][0]['fixedCounts']['OTHER']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts OTHER MODERATE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['OTHER']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts OTHER SEVERE

        metric = str(iq_app['aggregations'][0]['fixedCounts']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #fixedCounts OTHER CRITICAL

        metric = str(iq_app['aggregations'][0]['fixedCounts']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"fixedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #waivedCounts

        #waivedCounts SECURITY LOW

        metric = str(iq_app['aggregations'][0]['waivedCounts']['SECURITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts SECURITY MODERATE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['SECURITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Medium\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #waivedCounts SECURITY SEVERE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['SECURITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #waivedCounts SECURITY CRITICAL

        metric = str(iq_app['aggregations'][0]['waivedCounts']['SECURITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Security\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #waivedCounts LICENSE LOW

        metric = str(iq_app['aggregations'][0]['waivedCounts']['LICENSE']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #waivedCounts LICENSE MODERATE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['LICENSE']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts LICENSE SEVERE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts LICENSE CRITICAL

        metric = str(iq_app['aggregations'][0]['waivedCounts']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
					
        #waivedCounts QUALITY LOW

        metric = str(iq_app['aggregations'][0]['waivedCounts']['QUALITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts QUALITY MODERATE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['QUALITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts QUALITY SEVERE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['QUALITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts QUALITY CRITICAL

        metric = str(iq_app['aggregations'][0]['waivedCounts']['QUALITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts OTHER LOW

        metric = str(iq_app['aggregations'][0]['waivedCounts']['OTHER']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts OTHER MODERATE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['OTHER']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts OTHER SEVERE

        metric = str(iq_app['aggregations'][0]['waivedCounts']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #waivedCounts OTHER CRITICAL

        metric = str(iq_app['aggregations'][0]['waivedCounts']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"waivedCounts\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #openCountsAtTimePeriodEnd


        #openCountsAtTimePeriodEnd SECURITY LOW

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Security\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd SECURITY MODERATE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Security\",\"u_choice_1\":\"Medium\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #openCountsAtTimePeriodEnd SECURITY SEVERE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Security\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #openCountsAtTimePeriodEnd SECURITY CRITICAL

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Security\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #openCountsAtTimePeriodEnd LICENSE LOW

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['LICENSE']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"License\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)


        #openCountsAtTimePeriodEnd LICENSE MODERATE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['LICENSE']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"License\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd LICENSE SEVERE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd LICENSE CRITICAL

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['LICENSE']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"License\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
					
        #openCountsAtTimePeriodEnd QUALITY LOW

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['QUALITY']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd QUALITY MODERATE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['QUALITY']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd QUALITY SEVERE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['QUALITY']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd QUALITY CRITICAL

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['QUALITY']['CRITICAL'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Quality\",\"u_choice_1\":\"Critical\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd OTHER LOW

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['OTHER']['LOW'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Other\",\"u_choice_1\":\"Low\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd OTHER MODERATE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['OTHER']['MODERATE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Other\",\"u_choice_1\":\"Moderate\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd OTHER SEVERE

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #openCountsAtTimePeriodEnd OTHER CRITICAL

        metric = str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['OTHER']['SEVERE'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"openCountsAtTimePeriodEnd\",\"violation_type\":\"Other\",\"u_choice_1\":\"Severe\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

        #evaluationCount

        metric = str(iq_app['aggregations'][0]['evaluationCount'])
        data_opts = "{\"iq_application\":\"" + sn_sys_id_app + "\",\"iq_organization\":\""+ sn_sys_id_org + "\",\"metric\":\""+ metric + "\",\"u_choice_2\":\"none\",\"violation_type\":\"none\",\"u_choice_1\":\"none\",\"time_period_start\":\""+ date_start + "\"}"
        sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)

       # print (iq_app['applicationName'] + ', For week ' + str(counter) + ' there are ' + str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['CRITICAL']) + ' open scritical violations')
    print(counter)