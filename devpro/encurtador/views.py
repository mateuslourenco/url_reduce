from django.shortcuts import render, redirect


def redirecionar(request, slug):
    return redirect('http://google.com')
