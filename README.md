
# Transaction Using Django

Transaction should be done carefully without losing money. What happens if a sender sends money that didn't receive at the other and the money got deducted from sender's account.

That's  when the ACID property of django comes into play.




## Implementation

while writing the code for the transactions wrap up the code inside the " with transaction.atomic() " context processor or use transaction.atomic decorator 



```bash
  from django.db import transaction


  with transaction.atomic(): #either everything will work or none will work
            try:
                
                if sender_account.balance < int(amount):
                    messages.error(request, 'Insufficient balance.')
                    return redirect('index')
                sender_account.balance -= int(amount)
                sender_account.save()
                receiver_account.balance += int(amount)
                receiver_account.save()
                messages.success(request, 'Transfer successful')
                return redirect('index')
            except Account.DoesNotExist:
                messages.error(request, 'Account does not exist')
                return redirect('index')
            except Exception as e:
                messages.error(request, 'Transfer failed ' + str(e))
                return redirect('index')
```

if multiple transactions are happening at the same time,then we have to 
        isolate database for a single transaction only( use select_for_update() 
        along with transaction.atomic() )


```bash
sender_account = Account.objects.select_for_update().get(name=sender)
        receiver_account = Account.objects.select_for_update().get(name=receiver)
        
        with transaction.atomic(): #either everything will work or none will work
            try:
                
                if sender_account.balance < int(amount):
                    messages.error(request, 'Insufficient balance.')
                    return redirect('index')
                sender_account.balance -= int(amount)
                sender_account.save()
                receiver_account.balance += int(amount)
                receiver_account.save()
                messages.success(request, 'Transfer successful')
                return redirect('index')
            except Account.DoesNotExist:
                messages.error(request, 'Account does not exist')
                return redirect('index')
            except Exception as e:
                messages.error(request, 'Transfer failed ' + str(e))
                return redirect('index')

```
