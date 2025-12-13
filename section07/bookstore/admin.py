from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):  # type: ignore[type-arg] # Missing type parameters for generic type "ModelAdmin"
    readonly_fields = ("slug",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "rating")
    list_display = ("title", "author")


# admin.site.register(Book, BookAdmin)
