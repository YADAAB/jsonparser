import json
from Validator import Validator
from datetime import datetime

def isEighteen(line_obj, birth_date, created_at):
	"""
	validates if the customer is above 18 when the record was created
	"""
	creation_dt = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S')
	birth_dt = datetime.strptime(birth_date, '%m/%d/%Y')
	if int((creation_dt - birth_dt).days/365) < 18:
		line_obj.error_dict['isEighteen'] = False

def hasValidId(line_obj):
	"""
	validates if the phone#, email and zip code are valid(regex pattern match and length match) and not null
	"""
	err_dict_keys = line_obj.error_dict.keys()
	if 'phone' in err_dict_keys or 'zip5' in err_dict_keys or 'email' in err_dict_keys:
		 line_obj.error_dict['hasValidId'] = False

def schemaValidate(line_dict, schema_data):
	"""
	Consumes schema_data dict and validates data types and field specifications as mentioned in schema.json by invoking Validator() instance methods
	Returns a dictionary, error_dict that contains key, value pairs corresponding to the schema mismatches observed in each json record
	"""
	line_obj = Validator(line_dict)
	for key in schema_data['properties'].keys():
		key_type = schema_data['properties'][key]['type']
		if schema_data['properties'][key]['is_required'] == "yes" and line_obj.line_dict.get(key, 'NA') == 'NA':
			line_obj.error_dict[key] = "Null Data Entry"
			continue
		if key_type == "string":
			line_obj.isVarchar(key, schema_data['properties'][key].get('field_len', None))
		elif key_type == "int":
			line_obj.isDigit(key, schema_data['properties'][key].get('field_len', None))
		elif key_type == "email":
			line_obj.isValidEmail(key)
		elif key_type == "datetime":
			line_obj.isDateTime(key, schema_data['properties'][key]['date_format'])
		elif key_type == "enum":
			line_obj.isValidEnum(key, schema_data['properties'][key]['enum_list'])
		else:
			pass
	if line_obj.error_dict.get('birth_date', 'NA') == 'NA' and line_obj.error_dict.get('created_at', 'NA') == 'NA':
		#run isEighteen check only if Birth_Date and created_at are valid and not null
		isEighteen(line_obj, line_obj.line_dict['birth_date'], line_obj.line_dict['created_at'])
	hasValidId(line_obj)
	return line_obj.error_dict


if __name__ == "__main__":
	"""
	Parse the schema.json and open input stream from input json file.
	call the schema_validate() to validate each record and redirect to processed_data.json/anamoliies.json based on the error_dict return types
	"""
	print ("Inside Data Validator")
	schema_file = open("schema.json")
	schema_data = json.load(schema_file)
	f_input, fw_clean, fw_error =  open(schema_data['input_json']), open(schema_data['clean_data'], "w+"), open(schema_data['anamolies_data'], "w+")
	curr_id = -9999  #initialized curr_id to an unfeasible int to kick off validation of auto-increment of id column
	for line in f_input:
		line_dict = json.loads(line)
		error_dict = schemaValidate(line_dict, schema_data)
		if int(line_dict['id']) <= curr_id:
			error_dict['isIdAutoIncrement'] = False
		if len(error_dict.keys()) == 1:
			json.dump(line_dict, fw_clean)
			fw_clean.write('\n')
		else:
			error_dict['line_dict'] = line_dict
			json.dump(error_dict, fw_error)
			fw_error.write('\n')
		curr_id = int(line_dict['id'])
	f_input.close()
	fw_clean.close()
	fw_error.close()
	print ('Done..')
