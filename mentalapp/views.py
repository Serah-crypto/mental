# ================================================================
#  mentalapp/views.py
# ================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# ── MODELS ─────────────────────────────────────────────────────
from .models import Mood, JournalEntry, SavedResource, Checklist, UserProfile, ContactMessage

# ── FORMS ──────────────────────────────────────────────────────
from .forms import (
    UserRegisterForm,
    UserProfileForm,
    LoginForm,
    MoodForm,
    JournalForm,
    ChecklistForm,
    SavedResourceForm,
    ContactMessageForm,
)


# ── HOME & INFO PAGES ──────────────────────────────────────────
def home_view(request):
    return render(request, 'mentalapp/index.html')

def about(request):
    return render(request, 'mentalapp/about.html')

def conditions(request):
    return render(request, 'mentalapp/conditions.html')

def signs(request):
    return render(request, 'mentalapp/signs.html')

def prevention(request):
    return render(request, 'mentalapp/prevention.html')
def selfcare_info(request):
    return render(request, 'mentalapp/selfcare.html')

def resources_info(request):
    return render(request, 'mentalapp/resources.html')



def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            messages.success(request, "Your message has been sent!")
            return redirect('mentalapp:home')
    else:
        form = ContactMessageForm()
    return render(request, 'mentalapp/contact.html', {'form': form})


# ── AUTHENTICATION ─────────────────────────────────────────────
def register_view(request):
    # If the user is already logged in, send them to home
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('mentalapp:home')  # safe redirect

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in the user immediately
            messages.success(request, "Registration successful! Welcome 🎉")
            return redirect('mentalapp:home')  # redirect after registration
    else:
        form = UserRegisterForm()

    return render(request, 'mentalapp/register.html', {'form': form})


def login_view(request):
    # Redirect logged-in users to home
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('mentalapp:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Use next_url if provided, else redirect to home
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('mentalapp:home')  # redirect to home after login
        else:
            messages.error(request, "Invalid username or password.")

    # Pass 'next' from GET to template
    return render(request, 'mentalapp/login.html', {'next': request.GET.get('next', '')})

def logout_view(request):
    # FIX: Only allow POST logout to prevent CSRF/logout attacks
    if request.method == 'POST':
        logout(request)
        return redirect('mentalapp:home')
    return redirect('mentalapp:home')


# ── DASHBOARD ──────────────────────────────────────────────────
@login_required
def dashboard(request):
    today = timezone.now().date()
    recent_moods    = Mood.objects.filter(user=request.user).order_by('-date')[:5]
    recent_journals = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:3]
    today_checklist = Checklist.objects.filter(user=request.user, date=today).first()

    context = {
        'recent_moods':    recent_moods,
        'recent_journals': recent_journals,
        'today_checklist': today_checklist,
        'today':           today,
    }
    return render(request, 'mentalapp/dashboard.html', context)


# ── MOOD TRACKER ───────────────────────────────────────────────
@login_required
def mood_list(request):
    moods = Mood.objects.filter(user=request.user).order_by('-date')
    return render(request, 'mentalapp/mood_list.html', {'moods': moods})


@login_required
def mood_create(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, "Mood logged!")
            return redirect('mentalapp:mood_list')
    else:
        form = MoodForm(initial={'date': timezone.now().date()})
    return render(request, 'mentalapp/mood_form.html', {'form': form, 'action': 'Log'})


@login_required
def mood_edit(request, pk):
    mood = get_object_or_404(Mood, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MoodForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            messages.success(request, "Mood updated!")
            return redirect('mentalapp:mood_list')
    else:
        form = MoodForm(instance=mood)
    return render(request, 'mentalapp/mood_form.html', {'form': form, 'action': 'Edit'})


@login_required
def mood_delete(request, pk):
    mood = get_object_or_404(Mood, pk=pk, user=request.user)
    if request.method == 'POST':
        mood.delete()
        messages.success(request, "Mood entry deleted.")
        return redirect('mentalapp:mood_list')
    return render(request, 'mentalapp/mood_confirm_delete.html', {'mood': mood})


# ── JOURNAL ────────────────────────────────────────────────────
@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mentalapp/journal_list.html', {'entries': entries})


@login_required
def journal_create(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Journal entry saved!")
            return redirect('mentalapp:journal_list')
    else:
        form = JournalForm()
    return render(request, 'mentalapp/journal_form.html', {'form': form, 'action': 'New'})


@login_required
def journal_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    return render(request, 'mentalapp/journal_detail.html', {'entry': entry})


@login_required
def journal_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JournalForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Journal entry updated!")
            return redirect('mentalapp:journal_list')
    else:
        form = JournalForm(instance=entry)
    return render(request, 'mentalapp/journal_form.html', {'form': form, 'action': 'Edit'})


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Journal entry deleted.")
        return redirect('mentalapp:journal_list')
    return render(request, 'mentalapp/journal_confirm_delete.html', {'entry': entry})


# ── SELF-CARE CHECKLIST ────────────────────────────────────────
@login_required
def checklist_today(request):
    today = timezone.now().date()
    checklist, created = Checklist.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, "Checklist updated!")
            return redirect('mentalapp:checklist_today')
    else:
        form = ChecklistForm(instance=checklist)

    return render(request, 'mentalapp/checklist_today.html', {
        'form':      form,
        'checklist': checklist,
        'today':     today,
        'created':   created,
    })


@login_required
def checklist_history(request):
    items = Checklist.objects.filter(user=request.user).order_by('-date')
    return render(request, 'mentalapp/checklist_history.html', {'items': items})


# ── SAVED RESOURCES ────────────────────────────────────────────
@login_required
def saved_resources(request):
    resources = SavedResource.objects.filter(user=request.user)
    return render(request, 'mentalapp/saved_resources.html', {'resources': resources})


@login_required
def save_resource(request):
    if request.method == 'POST':
        form = SavedResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            messages.success(request, "Resource saved!")
            return redirect('mentalapp:saved_resources')
    else:
        form = SavedResourceForm()
    return render(request, 'mentalapp/save_resource_form.html', {'form': form})


@login_required
def delete_saved_resource(request, pk):
    resource = get_object_or_404(SavedResource, pk=pk, user=request.user)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource removed.")
        return redirect('mentalapp:saved_resources')
    return render(request, 'mentalapp/saved_resource_confirm_delete.html', {'resource': resource})


# ── PROFILE ────────────────────────────────────────────────────
@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'mentalapp/profile.html', {'profile': profile_obj})


@login_required
def profile_edit(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('mentalapp:profile')
    else:
        form = UserProfileForm(instance=profile_obj)
    return render(request, 'mentalapp/profile_edit.html', {'form': form})