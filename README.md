# jsonparser
Appl to read JSON data, input schema of the data to parse clean json records from anamolies 

# requirements
A company started business in 2013 and immediately started onboarding members.  

- Business rules:
You must be 18 years or older to have an account at Company
You must provide valid identifiers (email, zip code, phone number) during enrollment.
Members should never be removed (i.e. deleted), they should be marked as cancelled.
Attached is a DB schema for storing the input, the data should conform completely to the schema.

- Issue
Over the years, there are some bugs introduced into data like schema mismatch(int in the place of string), wrong inputs(like 8 digits in phone# instead of 10) etc

- Task
Read the input json and write an app. to identify clean data that adheres to the schema defined in the table below and follows above business rules. 
 
- Schema
create table members (
  id int not null auto_increment,
  first_name varchar(255) not null,
  last_name varchar(255) not null,
  email varchar(255) not null,
  phone int(10) not null,
  status enum('active', 'cancelled') not null,
  zip5 int(5) not null,
  created_at datetime,
  updated_at datetime,
  birth_date date not null);


# Solution Outline
Basically, I have take a meta-data driven approach for this problem. There is schema.json file that defines input fields with information like type, length and other restrictions that are applicable. Schema file also contains the path to input json file that needs to be cleaned up, output files where clean data is persisted once it is processed through all business rules and another file to store anamolies with error codes along with corresponding json record. 

Validator.py is the class that validates each record against business rules. For each record in the input(in customer_json_processor.py), a validator object is created with a variable initialized to the record. This then invokes right instance methods based on type obtained from schema file. I have an instance variable that holds error codes. Based on the output returned into the error code variable, I route my record to clean data file or anamolies file. 
