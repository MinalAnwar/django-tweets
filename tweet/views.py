from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegisterationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("created_at")
    return render(request, 'tweet/tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    #Either form is filled or not 
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save() 
            return redirect('tweet:tweet_list')
    else:
        form = TweetForm()
        
    return render(request, 'tweet/tweet_form.html', {'form' : form})

@login_required        
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == "POST":
        #instance get the tweet which we are editing as we get at the top
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet:tweet_list')
    else:
        form = TweetForm(instance=tweet)
        
    return render(request, 'tweet/tweet_form.html', {'form' : form})

@login_required    
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet:tweet_list')
    return render(request, 'tweet/tweet_confirm_delete.html', {'tweet' : tweet})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet:tweet_list')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html', {'form' : form})