# PayApp

**[G6060] Web Applications and Services**

A web-based, multi-user payment service, essentially a simplified version of PayPal. 

Link to video walkthrough of application: https://youtu.be/SC0tpziKW-E 

Application URL: https://webapps2023.onrender.com/

## Application Description
During the registration process, users provide their username, first and last name, email address, and password. Each user has a single online account with a selected currency (GBP, USD, or Euros). The system automatically converts the initial amount based on the chosen currency.

Registered users can perform various transactions, such as transferring money, receiving payments, and managing their account balance. The system assumes users start with a specified amount of money and does not involve connections to real financial sources.

Users can initiate direct payments to other registered users, and if the request is accepted and funds are sufficient, the money is immediately transferred. Users can also request payments from other users while also being able to respond accordingly to incoming requests by rejecting the request or accepting to send the payment.

The system enables users to view their transaction history, including sent and received payments and payment requests, as well as their current account balance. Administrators have access to all user accounts, transactions, and can register additional administrators.

Additionally, a separate RESTful web service is implemented to handle currency conversion. The service responds to GET requests and provides conversion rates between currencies.
