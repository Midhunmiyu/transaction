
# Transaction Using Django

Transaction should be done carefully without losing money. What happens if a sender sends money that didn't receive at the other and the money got deducted from sender's account.

That's  when the ACID property of django comes into play.




## Implementation

while writing the code for the transactions wrap up the code inside the " with transactions.atomic() " context processor or use transaction.atomic decorator 

***from django.db import transaction***
