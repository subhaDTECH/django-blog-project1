from django.shortcuts import render,HttpResponseRedirect
from .forms import  SignUpForm,LoginForm,postForm
from django.contrib import  messages
from django.contrib.auth import authenticate,login,logout
from .models import post


# Create your views here.
def home(request):
    data=post.objects.all()
    return render(request,'blog/home.html',{"form":data})


def about(request):
    return render(request,'blog/about.html') 


def contact(request):
    return render(request,'blog/contact.html') 


def user_signup(request):
    if request.method =="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"you become an author ")
            form.save()
            
    else:
        form=SignUpForm()

    
    return render(request,'blog/signup.html',{"form":form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"you have successfully login")
                    return HttpResponseRedirect('/dashboared/')
        else:
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboared/')

            
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')            
              
def dashboared(request):
    if request.user.is_authenticated:
        posts=post.objects.all()
        return render(request,'blog/dashboared.html',{'post':posts})
    else:
        return HttpResponseRedirect('/login/')




# curd operation on dashboared 
def add_post(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            form=postForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=post(title=title,desc=desc)
                pst.save()
                form=postForm()
                return HttpResponseRedirect('/')
        else:
            form=postForm()        
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')  

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method =="POST":
            pi=post.objects.get(pk=id)
            form=postForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"update successfully")
                return HttpResponseRedirect('/dashboared/')
           
        else:
            pi=post.objects.get(pk=id) 
            form=postForm(instance=pi)      
        return render(request,'blog/updatepost.html',{'form':form})  
    else:
        return HttpResponseRedirect('/login/')
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi=post.objects.get(pk=id)
            pi.delete()
        return render(request,'blog/deletepost.html')  
    else:
        return HttpResponseRedirect('/login/')
