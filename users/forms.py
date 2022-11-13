from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

from .models import Profile,GisData


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
        


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        

class FileUploadForm(forms.ModelForm):
    # # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    title = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control w-100','placeholder':'Title of this dataset.'}))
    metadata = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100', 'rows': 10,'placeholder':'Write a brief metadata about the dataset.'}))
    category = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control w-100','placeholder':'The category of data eg: Climate change, Population, Water sources etc'}))
    tags = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control w-100','placeholder':'use comma separation eg. gis,ml,data science'}))
    data_projection = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control w-100','placeholder':'Specify Dataset coordinate system if any, in this format: EPSG:4326, EPSG:32737, EPSG:32637'}))
    
    class Meta:
        model = GisData
        exclude = ('gis_data_type','gis_data_key','user','status','publish',)
        # exclude = ('user',)
        fields = ['title','metadata','tags','category','data_projection']
        # fields = '__all__'
        
    