def xss_lab3(request):
    if request.user.is_authenticated:
        return render(request, 'Lab/XSS/xss_lab_3.html')
    else:
        return redirect('login')