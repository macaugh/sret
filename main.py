from log import log_message
from sf import SFExploit
from datetime import date
import sys

def salesforce_tester(url):
	log_message(f"> Testing: {url}")
	vulnerability = {'accessible_objects':[],
					'writable_objects':[]}
	got_objects = list()
	tester = SFExploit(url)
	if tester.invalid:
		return {'vulnerable':False}
	available_objects = tester.get_objects()

	# test unauth object access
	log_message(f">> Testing unauth objects.")
	for object_name in available_objects:
		object_data = tester.get_object_items(object_name)
		if object_data: # something was returned:
			log_message(f">>> Found {object_name} to be accessible.")
			object_data_metric = {object_name:{'total_count':object_data['totalCount']}}
			vulnerability['accessible_objects'].append(object_data_metric)
			got_objects.append(object_name)

	# test unauth write
	log_message(f">> Testing unauth write to objects")
	for object_name in available_objects:
		write_allowed  = tester.attempt_record_create(object_name)
		if write_allowed:
			log_message(f">>> Found {object_name} to be potentially vulnerable.")
			vulnerability['writable_objects'].append(object_name)
	
	if len(vulnerability['accessible_objects']) > 0 or len(vulnerability['writable_objects']) > 0:
		log_message(f">> Concluding testing for {url}. {url} is vulnerable.")
		final_return = {'vulnerable':True, 'data':vulnerability}
		return final_return
	else:
		log_message(f">> Concluding testing for {url}. {url} is not vulnerable")
		return {'vulnerable':False}

def main(url):
    today = date.today()
    formatted_date = today.strftime("%m/%d/%Y")
    log_message(f"Scan date: {formatted_date}")
    vulnerability_rating = salesforce_tester(url)
    return vulnerability_rating

if __name__ == "__main__":
    url = sys.argv[1]
    main(url)










