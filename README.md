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


#*To run Project*

##First
install Docker on your machine you can follow the steps [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
##Second 
cd to folder of project 

- cd LenmoTest
-  docker-compose  up --build 

if open project for first time use "*docker-compose  up --build*" , if you use it before without change the code or
 setting of docker file
 or docker-compose you can just use "*docker-compose  up*" 

