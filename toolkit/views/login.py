from django.shortcuts import render
from django.views import View
# from .models import Account


class Login(View):
    def get(self, request):
        return render(request, "login.html")
        
    def post(self, request):
        formEmail = request.POST['email']
        formPassword = request.POST['password']
        valid = retrieve_user(formEmail, formPassword)
        if valid:
            return redirect('/home/')
        return render(request, "login.html")
    
    # Function used to retrieve User from given email address or username and validate password
    def retrieve_user(self, formEmail, formPassword):
        try:
            e = Account.objects.get(email=formEmail)
            isValid = (e.password == formPassword)
        except:
            return False
        if isValid:
            return True
        return False
        


            












