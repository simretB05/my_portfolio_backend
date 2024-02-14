def check_endpoint_info(sent_data, expected_data):
    for data  in expected_data:
        if(sent_data.get(data) == None):
            return fThe {data} must be sent! 
