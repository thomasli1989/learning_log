from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
    #logout
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    #register new user
    if request.method != 'POST':
        #show empty form
        form = UserCreationForm()
    else:
        form =UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #let user login auto and reverse to index page
            authenticate_user = authenticate(username=new_user.username,password = request.POST['password1'])
            login(request,authenticate_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form':form}
    return render(request,'register.html',context)