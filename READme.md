Thanks for this opportunity!

I have done the task required.

Please note that you will need to createsuperuser and makemigrations and migrate.

you can register normail users from router register.

you will need to specify the fees in views constant at top.

Please note any request requires to use basic authorization using email and password.

POST
after creating users you can choose to be borrower or investor from the first two urls.

POST
after that when you send request to placeloan you will need to include in request.body(loan_amount,loan_period)

GET
after that the investors can get the available loans from /Available-loans/ 

POST
they can propose using /Propose/ you will need to include in the request body (loan_id)

GET
borrower can get all of the proposals from /Get-proposal/


PATCH
Also can accept specific proposal from /Accept-proposal/ please note that he needs to include in the request body ('loan_id','investor_id'')

PATCH
after every monthly payment he check from /Accepted-payment/