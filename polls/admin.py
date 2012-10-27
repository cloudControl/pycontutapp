from polls.models import Poll
from django.contrib import admin
from polls.models import Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(PollAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date', 'exp_date', 'finished'], 'classes': ['collapse']}),
        ('Editor information', {'fields': ['created_by'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently', 'is_expired', 'finished', 'created_by')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)
