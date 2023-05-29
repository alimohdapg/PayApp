# webapps2023

**[G6060] Web Applications and Services**

A web-based, multi-user payment service, essentially a simplified version of PayPal. 

## Application Description
During the registration process, users provide their username, first and last name, email address, and password. Each user has a single online account with a selected currency (GBP, USD, or Euros). The system automatically converts the initial amount based on the chosen currency.

Registered users can connect their online accounts and perform various transactions, such as transferring money, receiving payments, and managing their account balance. The system assumes users start with a specified amount of money and does not involve connections to real financial sources.

Users can initiate direct payments to other registered users, and if the request is accepted and funds are sufficient, the money is immediately transferred. Users can also request payments from other users and respond accordingly by rejecting the request or making a payment.

The system enables users to view their transaction history, including sent and received payments and payment requests, as well as their current account balance. Administrators have access to all user accounts, transactions, and can register additional administrators.

Additionally, a separate RESTful web service is implemented to handle currency conversion. The service responds to GET requests and provides conversion rates between currencies.
