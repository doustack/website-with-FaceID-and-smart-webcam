from django.shortcuts import render,redirect
from django.contrib import messages
from detection.Motion_detection import run_hand_detection

def hand_admin_login(request):
    if not request.user.is_authenticated:
        messages.error(request,'You must log in to the site')
        return redirect('pages:matrix')
    if request.user.is_superuser:
        if run_hand_detection():
            messages.success(request,'Login')
            return redirect("/admin/")  
        else:
            messages.error(request,'Hand gesture not confirmed')
            return redirect('pages:matrix')
        
    return redirect('pages:matrix')
         

# Create your views here.
def home_grid(request):
    return render(request,"pages/home-grid.html",context={})


def home_matrix(request):
    return render(request,"pages/home-matrix.html",context={})


def home_neon(request):
    return render(request,"pages/home-neon.html",context={})