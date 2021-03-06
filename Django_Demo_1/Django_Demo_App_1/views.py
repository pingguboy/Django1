from django.shortcuts import render
from django.http import HttpResponse
from Django_Demo_App_1.models import AccessRecord,Topic,Webpage,UserProfileInfo,School,Student
from Django_Demo_App_1.forms import UserForm, UserProfileInfoForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
# Create your views here.

def index(request):
    context_dict={'text':'hello world','number':100}
    return render(request,"Django_Demo_App_1/index.html",context=context_dict)

def other(request):
    return render(request,'Django_Demo_App_1/other.html')

def relative(request):
    return render(request,'Django_Demo_App_1/relative_url.html')

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'Django_Demo_App_1/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        # IF USER IS AUTHETICATED
        if user:
            # IF USER IS ACTIVE
            if user.is_active:
                login(request,user)
                # REDIRECTED TO INDEX PAGE
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("INACTIVE ACCOUNT")
        else:
            print("Someone tried to login but failed, as usual... a very vivid example of that person's life, a failure.")
            return HttpResponse("INVALID")
    else:
        return render(request,'Django_Demo_App_1/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in")

class CBView(View):
    def get(self, request):
        return HttpResponse("CBV!!")

class IndexView(TemplateView):
    template_name='Django_Demo_App_1/index.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['templateview']='Vanakam'
        return context

class SchoolListView(ListView):
    model=School
    context_object_name='schools'

class SchoolDetailView(DetailView):
    context_object_name='school_detail'
    model=School
    template_name='Django_Demo_App_1/school_detail.html'

class SchoolCreateView(CreateView):
    model=School
    fields=('name','principal','location')
    # template_name='Django_Demo_App_1/school_form.html'

class SchoolUpdateView(UpdateView):
    model=School
    fields=('name','principal')

class SchoolDeleteView(DeleteView):
    model=School
    success_url=reverse_lazy('Django_Demo_App_1:list')
