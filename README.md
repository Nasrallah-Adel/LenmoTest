# Lenmo-Test
Use case\
\
A Lenmo borrower would like to borrower $5,000.00 on paying them back on 6 months period. One of Lenmo investors has offered him 15% Annual Interest Rate. A $3.00 Lenmo fee will be added to the total loan amount to be paid by the investor.  
 
Requirements:
You are required to develop a Django REST project to be able to build the following flow through its APIs;
 
1-The borrower creates a loan request including the above loan amount and loan period 
2-The investor will submit an offer for the borrower’s loan request with the above interest rate
3-The borrower will accept the offer
Check if the investor has sufficient balance in their account before they fund the loan
4-The loan will be funded successfully and the loan status will be Funded 
5-The loan payments will be created with the monthly amount to be paid and its due date
6-Once all the payments are successfully paid to the investor, the loan status will be Completed 


# *To run Project*

## First
install Docker on your machine you can follow the steps [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

## Second 


cd to folder of project 

- ``` cd LenmoTest```
-  ```docker-compose  up --build``` 

if open project for first time use "*```docker-compose  up --build```*" , if you use it before without change the 
 setting of docker file
 or docker-compose you can just use "*```docker-compose  up```*" 
 
 ## after run project
 -  open your browser and type [lenmo.loclhost](lenmo.loclhost)
 - the project will open on swagger documentation of APIS
 
 # Note 
 ## You won't see anything of API'S Until Authenticate who you are 
 
 ## 10 type of user exist [BORROWER , INVESTOR ]
 ## when yo login as  *BORROWER* you can use only API'S belong to  *BORROWER* and  when yo login as *INVESTOR* you can use only API'S belong to *INVESTOR*
 

 # use case
 #### first you need make two account one as *borrower* and second as investor 
 
 - open your browser  after run docker-compose and type [lenmo.localhost](lenmo.localhost)
 
 ![first](documentation/1.png)
 
 -  make BORROWER account from register
 
![first](documentation/2.png)
![first](documentation/3.png)
- after register save token of user to use it or you can get it by email and password from api-token link
![first](documentation/6.png)
![first](documentation/7.png)

-  make INVESTOR account from register
![first](documentation/4.png)
![first](documentation/5.png)
- after register save token of user to use it or you can get it by email and password from api-token link
![first](documentation/12.png)
![first](documentation/7.png)

-  use authorize button to authorize your self and use api's

- we use JWT authentication 
![first](documentation/8.png)
- use your token like this
```JWT eyJ0eXAiOiJKV1QiLCJhbGciOi```
- and click on authorize button
![first](documentation/9.png)

- you will find API's appear for BORROWER
![first](documentation/10.png)
![first](documentation/11.png)

-use rhe same steps for INVESTOR get INVESTOR token and authorize by it and you will find INVESTOR APIS

![first](documentation/12.png)

![first](documentation/7.png)

![first](documentation/8.png)

![first](documentation/9.png)

![first](documentation/13.png)














