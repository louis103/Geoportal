from urllib.request import urlopen
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from botocore.exceptions import ConnectionError,ClientError,EndpointConnectionError, ConnectTimeoutError, ReadTimeoutError, ProxyConnectionError, ConnectionClosedError
from django.contrib import messages
from django.views import View
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .forms import RegisterForm, LoginForm, FileUploadForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from users.decorators import admin_only, allowed_users, unauthenticated_user

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.views import PasswordChangeView
from django.db.models import Count
from django.db.models import Q
import environ
import os

import csv
from django.http import HttpResponse

from boto3.session import Session
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

session = Session(
    region_name=env('REGION_NAME'),
    aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY')
)

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from .models import GisData, Profile, SendMessage

def home(request):
    return render(request, 'users/home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
    
    
# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')
    

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

# get all datasets in s3
import boto3
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket('gisdata-001')
def getDatasetsFromS3():
    my_files = []
    for object in my_bucket.objects.filter(Prefix='Datasets/'):
        my_files.append(object.key)
        
    return my_files
s3 = session.resource('s3')
ALLOWED_EXTENSIONS = ["7z","gz","rar","kml","jpg","jpeg","png","shp","geotiff","tif","tiff","geojson","json","pdf","csv","xlsx","zip"]
@allowed_users(allowed_roles=['admin'])
def s3_form(request):
    if request.method == "POST":
        file = request.FILES.get("file_field_single")
        filename = os.path.splitext(str(file))[0]
        extension = os.path.splitext(str(file))[1][1:]
        full_name = filename + "." + extension
        if extension in ALLOWED_EXTENSIONS:
            try:
                s3.Bucket(env('BUCKET_NAME')).put_object(Key='Datasets/{}'.format(full_name), Body=request.FILES['file_field_single']) 
                messages.success(request,f"File Uploaded successfully to Amazon S3 as: {full_name}")
                return redirect(to='file-upload')
            except ClientError as e:
                messages.error(request, f'Failed to Upload Dataset!') 
                return HttpResponse(f'Failed to upload Dataset due to {e}')
            except ConnectTimeoutError as e:
                messages.error(request, f'Failed to Upload Dataset!') 
                return HttpResponse(f'Failed to upload Dataset, Check your internet connection. {e}')
            except ConnectionClosedError as e:
                messages.error(request, f'Failed to Upload Dataset!') 
                return HttpResponse(f'Failed to upload Dataset, Check your internet connection. {e}')
            except ReadTimeoutError as e:
                messages.error(request, f'Failed to Upload Dataset!') 
                return HttpResponse(f'Failed to upload Dataset, Read Timeout Error. {e}')
            except ConnectionError as e:
                messages.error(request, f'Failed to Upload Dataset!') 
                return HttpResponse(f'Failed to upload Dataset, Connection Error. {e}')
        else:
            return HttpResponse(f'File Extension not allowed!')    
    else:
        all_available_datasets = getDatasetsFromS3()
        form  = FileUploadForm()
        context = {'form':form,'data': all_available_datasets}
        return render(request, "users/file_upload_form.html", context)
    
    
# filter, order and search
PRODUCTS_PER_PAGE = 2
def listProducts(request):
    
    ordering = request.GET.get('ordering', "")     # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")

    if search:
        product = GisData.objects.filter(Q(product_name__icontains=search) | Q(brand__icontains=search)) # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite

    else:
        product = GisData.objects.all()

    if ordering:
        product = product.order_by(ordering) 

    if price:
        product = product.filter(price__lt = price)
    

    # Pagination
    page = request.GET.get('page',1)
    product_paginator = Paginator(product, PRODUCTS_PER_PAGE)
    try:
        product = product_paginator.page(page)
    except EmptyPage:
        product = product_paginator.page(product_paginator.num_pages)
    except:
        product = product_paginator.page(PRODUCTS_PER_PAGE)
    return render(request, "firstapp/listproducts.html", {"product":product, 'page_obj':product, 'is_paginated':True, 'paginator':product_paginator})

# filter, order and search
PRODUCTS_PER_PAGE = 2
def get_all_datasets(request):
    ordering = request.GET.get('ordering', "")     # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    price = request.GET.get('type', "")
    category = request.GET.get('category', "")
    
    if search:
        # allow only approved datasets to be filtered
        datasets = GisData.objects.filter(status='APPROVED').filter(Q(title__icontains=search) | Q(metadata__icontains=search)).order_by('id') # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite

    else:
        datasets = GisData.objects.filter(status='APPROVED').order_by('id')

    if ordering:
        datasets = datasets.order_by(ordering) 

    if price:
        datasets = datasets.filter(gis_data_type = price)
        
    if category:
        datasets = datasets.filter(category = category)
    
    
    data_count = datasets.count()
    # search
    query = request.GET.get("q")
    # if query:
    #     datasets=GisData.objects.filter(status='APPROVED').filter(Q(title__icontains=query) | Q(metadata__icontains=query)).distinct()
    # pagination
    paginator = Paginator(datasets, 10) # 10 posts in each page
    page = request.GET.get('page', 1)
    try:
        datasets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        datasets = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        datasets = paginator.page(paginator.num_pages)
    # .order_by=('-created_at', '-pk')
    context = {'datasets': datasets,'data_count':data_count,'pages':page}
    return render(request, "users/list_all_datasets.html",context)

def view_single_dataset(request, pk):
    dataset_details = GisData.objects.get(id=pk)
    context = {'dataset_details': dataset_details}
    return render(request, "users/view_single_dataset.html", context)

from urllib.request import HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
import os
from pathlib import Path
s3 = session.resource('s3')
BASE_DIR = Path(__file__).resolve().parent.parent
FILEPATH = str(BASE_DIR) + '/media/'
AWS_GOOGLE_STORAGE = str(os.getenv('AWS_RESOURCE_LINK')) + "/google/"
def update_user_social_data(strategy, *args, **kwargs):
  response = kwargs['response']
  backend = kwargs['backend']
  user = kwargs['user']

  if response['picture']:
    url = response['picture']
    print("URL: ",url)
    userProfile_obj = user.profile
    avatar = urlopen(url).read()
    new_file = str(user.username + '.jpg')
    res = s3.Bucket(env('BUCKET_NAME')).put_object(Key='media/{}'.format(new_file), Body=avatar)
    if res:
        user_profile = new_file
    else:
        user_profile = "default.webp"
    userProfile_obj.user = user
    userProfile_obj.avatar = user_profile             
    userProfile_obj.save()
    
from rest_framework.decorators import api_view
# @api_view(['POST'])
def upload_data(request):
    if request.method == 'POST':
        data_form = FileUploadForm(request.POST, request.user)
        if data_form.is_valid():
            try:
                com_form = data_form.save(commit=False)
                # data_form.instance.user = request.user
                com_form.user = request.user
                print("Saving")
                com_form.save()
                # print(data_form)
                messages.success(request, f'Dataset and metadata uploaded successfully!')
                return redirect(to='list_datasets')
            except Exception as e:
                messages.error(request, f'Dataset Failed to Upload! due to {e}')
                return redirect(to='file-upload')
        else:
            messages.error(request, f'Form Invalid!')
            return redirect(to='file-upload') 
        
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def contact_us(request):
    context = {}
    if request.method == 'POST':
        cur_user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # add data to db
        reply = SendMessage(user=cur_user,name=name,email=email,message=message)
        reply.save()
        messages.success(request,"Your Message was submitted successfully!")
        return redirect(to='contact_us')
    
    return render(request, "users/contact.html", context)

# @login_required
def show_map(request):
    context = {}
    return render(request, "users/map.html", context)

from django.http import JsonResponse
def suggestionApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = GisData.objects.filter(Q(title__icontains=search))[0:10]
        titles = list()
        for item in qs:
            titles.append(item.title)
        return JsonResponse(titles, safe=False)
    

# download dataset here 
BUCKET_NAME = env('BUCKET_NAME')
s3_resource = session.resource("s3")
def download_dataset(request, pk):
    obj = GisData.objects.get(pk=pk)
    # filename = obj.gis_data_key
    filename = 'kenya-villages.csv'
    if request.method == 'GET':
        try:
            s3_resource.Bucket(BUCKET_NAME).download_file('Datasets/{}'.format(filename),filename)
            # ,f'/Downloads/{filename}'
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return Response({'message':f'File not Found within S3 Bucket!'}, status=status.HTTP_404_NOT_FOUND) 
            else:
                raise
    else:
        return Response({"message": "Method not allowed!"}, status=status.HTTP_403_FORBIDDEN)

def export_csv_metadata(request, pk):
    
    '''
    Here we query the dataset by id and download the metadata
    '''
    obj = GisData.objects.get(pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=metadata.csv'
    
    # headers = ['Title','Abstract','Attribution','Organization','License','Category','Projection','Spatial Extent','Tags','Data Type','Key Name','Status','Published At']
    headers = ['Metadata Information']
    writer = csv.writer(response)
    content = [
        f"Dataset Title; {obj.title}",
        f"Abstract; {obj.metadata}", 
        f"Attribution; {obj.attribution}", 
        f"Parent Organization; {obj.organization}",
        f"License; {obj.license}", 
        f"Category; {obj.category}",
        f"Dataset Projection; {obj.data_projection}", 
        f"Spatial Extent; {obj.spatial_extent}", 
        f"Tags; {obj.tags}", 
        f"Type of Dataset; {obj.gis_data_type}", 
        f"FileName; {obj.gis_data_key}", 
        f"Status; {obj.status}", 
        f"Published At; {obj.publish}"
    ]
    writer.writerow(headers)
    for value in content:
        writer.writerow([value])
    
    return response