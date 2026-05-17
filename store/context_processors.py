from .models import Category

def categories_context(request):
    return {
        'nav_categories': Category.objects.filter(is_active=True, parent=None).order_by('order')[:8]
    }
