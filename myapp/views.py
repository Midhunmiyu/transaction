from django.shortcuts import redirect, render
from django.views import View
from .models import Account
from django.contrib import messages
from django.db import transaction


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class TransferView(View):
    def post(self, request):
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        amount = request.POST.get('amount')
        
        '''
        if multiple transactions are happening at the same time,then we have to 
        isolate database for a single transaction only( use select_for_update() 
        along with transaction.atomic() )
        ''' 
        # sender_account = Account.objects.get(name=sender)
        # receiver_account = Account.objects.get(name=receiver)
        
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