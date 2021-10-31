# AddressFormatterAPI
This API was created to overcome the issue of repetitive words in Aadhaar address.

It will take json like the following as input

![image](https://user-images.githubusercontent.com/85789531/139593876-bd1bbbaf-17cb-4398-97c7-62a343d43a55.png)
And will give output as the following

![image](https://user-images.githubusercontent.com/85789531/139593879-a93f489f-0e73-456c-8261-441208515937.png)
![image](https://user-images.githubusercontent.com/85789531/139593886-be3a4844-6058-4655-a572-076720d17c30.png)

Steps to run :
->Download FastApi and Python3.
->Download the code.
->Go to the folder where the code is stored and run python -m uvicorn AddressFormatterAPI:app --reload in command prompt.
->Go to localtest.me:8000/format_address?access_token=UIDAI12345
->UIDAI12345 is the API key.
->Go to Post format_address and click try it out.
->Give the address and execute it.
