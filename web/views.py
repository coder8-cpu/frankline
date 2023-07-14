from django.shortcuts import render,redirect
from .models import *
# Create your views here.


class index(object):
    def __init__(self) -> None:
        pass
    
    def show_index(self,request):
        return render(request,"index.html")
    
class contact(object):
    def __init__(self) -> None:
        pass
    
    def show_contact(self,request):
        return render(request,"contact.html")
    def post_data(self,request):
        data = request.POST

        obj = Contact()
        obj.name = data.get('username')
        obj.mobileno = data.get('mobileno')
        obj.inquery = data.get('typeContact')
        obj.email = data.get('email')
        obj.msg = data.get('msg')
        obj.save()
        return redirect("/") 
        
    
class dealership(object):
    def __init__(self) -> None:
        pass
    
    def show_dealership(self,request):
        return render(request,"dealership.html")
    
    def post_data(self,request):
        data = request.POST
        obj = Dealer()
        obj.name = data.get('dname')
        obj.mobileno = data.get('dmobileno')
        obj.city = data.get('city')
        obj.email = data.get('email')
        obj.msg = data.get('msg')
        obj.save()
        return redirect("/") 

        
    
class render_popup(object):
    def __init__(self) -> None:
        pass
    def show_popup(self,request):
        return render(request,"popup.html")
    

    
