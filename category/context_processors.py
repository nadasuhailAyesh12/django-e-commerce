from .models import Category

def menu_links (request):
    menu_categories = Category.objects.all()
    return { 'menu_categories': menu_categories }