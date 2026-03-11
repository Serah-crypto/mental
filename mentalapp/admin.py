from django.contrib import admin
from .models import UserProfile, Mood, JournalEntry, Checklist, SavedResource, ContactMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display  = ('user', 'mood_score', 'date', 'created_at')
    list_filter   = ('mood_score', 'date')
    search_fields = ('user__username',)
    date_hierarchy = 'date'


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'title', 'is_private', 'created_at')
    list_filter   = ('is_private',)
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display  = ('user', 'date', 'completion_score_display', 'completion_percent_display')
    search_fields = ('user__username',)
    date_hierarchy = 'date'

    def completion_score_display(self, obj):
        return f"{obj.completion_score}/11"
    completion_score_display.short_description = 'Items Completed'

    def completion_percent_display(self, obj):
        return f"{obj.completion_percent}%"
    completion_percent_display.short_description = 'Completion %'


@admin.register(SavedResource)
class SavedResourceAdmin(admin.ModelAdmin):
    list_display  = ('user', 'title', 'resource_type', 'saved_at')
    list_filter   = ('resource_type',)
    search_fields = ('user__username', 'title')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = 'Mark selected messages as read'