import json
from datetime import datetime
import re 

class Validator:

	def __init__(self, line_dict = None):
		self.line_dict = line_dict
		self.error_dict = {"id":line_dict["id"]}

	def putExceptionMsg(self, field_name, excep_msg):
		"""
		Helper fn to generate Exceptioon Messages
		"""
		self.error_dict[field_name] = str(self.error_dict.get(field_name, '')) + excep_msg

	def isVarchar(self, field_name, field_len = None):
		"""
		Validates if field_name is valid str and less than field_length, and not null
		"""
		try:
			if field_len and len(self.line_dict[field_name]) > field_len:
				self.putExceptionMsg(field_name, 'Invalid varchar field length')
				return False
			if isinstance(self.line_dict[field_name], str):
				return True
			else:
				self.putExceptionMsg(field_name, 'Invalid datatype')
		except Exception as e:
			self.putExceptionMsg(field_name, str(e)[:50])
		return False

	def isValidEnum(self, field_name, enum_list):
		"""
		validates if the field_value is allowed in enum list of occurences
		"""
		try:
			if self.line_dict[field_name] not in enum_list:
				self.putExceptionMsg(field_name, 'Invalid Enum List of Values')
		except Exception as e:
			self.putExceptionMsg(field_name, str(e)[:50])


	def isDigit(self, field_name, field_len = None):
		"""
		Validates if field_name is valid int , and not null
		"""
		try:
			if field_len and len(self.line_dict[field_name]) != field_len:
				self.putExceptionMsg(field_name, 'Invalid field length')
				return False
			if isinstance(int(self.line_dict[field_name]), int):
				return True
			else:
				self.error_dict[field_name] = str(self.error_dict.get(field_name, '')) + 'Invalid datatype'
		except Exception as e:
			self.putExceptionMsg(field_name, str(e)[:50])
		return False


	def isValidEmail(self, field_name):
		"""
		Validates if given field has valid email using regex patterns
		"""
		email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		try:
			if(re.search(email_regex,self.line_dict[field_name])):
				return True
			else:
				self.error_dict[field_name] = str(self.error_dict.get(field_name, '')) + 'Invalid email'
		except Exception as e:
			self.putExceptionMsg(field_name, str(e)[:50])
		return False


	def isDateTime(self, field_name, date_format):
		"""
		Validates if field_name is valid Date, and not null
		"""
		try:
			dt = datetime.strptime(self.line_dict[field_name], date_format)
			return True
		except Exception as e:
			self.putExceptionMsg(field_name, str(e)[:50])
		return False
