# AddressFormatterAPI
This API was created to overcome the issue of repetitive words in Aadhaar address.<br />

It will take json like the following as input<br />

![image](https://user-images.githubusercontent.com/85789531/139593876-bd1bbbaf-17cb-4398-97c7-62a343d43a55.png)<br />
And will give json output as the following<br />

![image](https://user-images.githubusercontent.com/85789531/139593879-a93f489f-0e73-456c-8261-441208515937.png)<br />
![image](https://user-images.githubusercontent.com/85789531/139593886-be3a4844-6058-4655-a572-076720d17c30.png)<br />

Screen Capture - https://youtu.be/ltjOmxLjL2w![image](https://user-images.githubusercontent.com/85789531/139594488-856f376e-0b04-43ab-931c-c7b3317e45ec.png)

Steps to run :<br />
->Download FastApi and Python3.<br />
->Download the code.<br />
->Go to the folder where the code is stored and run python -m uvicorn AddressFormatterAPI:app --reload in command prompt.<br />
->UIDAI12345 is the API key and localtest.me is the domain<br />
->Go to http://localtest.me:8000/format_address?access_token=UIDAI12345#/<br />
->Go to Post 'format_address' and click 'try it out'<br />
->Give the address in request body and execute it.<br />
->Optionally, Address in local lannguage can also be provided. <br />
->Formatted Address will be there in Response body<br />
