from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class PostForm(forms.ModelForm):
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        required=True, 
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Post
        exclude = ('publish_date','user', 'last_modified', 'likes')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the content'
            
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-control'
            }),
        }
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ('post', 'user', 'publish_date')
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',  
                'placeholder': 'Enter your comment here...', 
                'rows': 5, 
            })
        }
        
class SignUpForm(forms.ModelForm):
    
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={    
            'class': 'form-control',
            'placeholder': 'Enter your email...',
            })
        }
        
class User_Registration(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email...'}))
    
    first_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={    
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            }))
    last_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={    
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            }))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2',]
        
    def __init__(self, *args, **kwargs) :
        super(User_Registration, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    

class ProfileForm(forms.ModelForm):
    
    country_list = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
        "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
        "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
        "Congo, Republic of the", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
        "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
        "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
        "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
        "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
        "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
        "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro",
        "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria",
        "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
        "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
        "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
        "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
        "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago",
        "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
        "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    
    country = forms.ChoiceField(choices=[(country, country) for country in country_list], widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    
    class Meta:
        
        model = UserProfile
        fields = ['avatar', 'country', 'bio']
        
        widgets = {
            'bio': forms.Textarea(attrs={    
            'class': 'form-control',
            'placeholder': 'Add bio',
            }),
            'country': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class EditProfile(UserChangeForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email...'}))
    
    first_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={    
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            }))
    last_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={    
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            }))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username',]
        
    def __init__(self, *args, **kwargs) :
        super(EditProfile, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'