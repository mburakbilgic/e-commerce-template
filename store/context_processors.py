from .models import Category


def categories(request):
    return {
      'categories': Category.objects.prefetch_related(
            'children',
            'children__children',
            'children__children__children',
        ).filter(parent__isnull=True)
    }
