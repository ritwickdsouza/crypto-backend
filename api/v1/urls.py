from django.urls import path

from api.v1.views import QuotesAPIViewSet

urlpatterns = [
    path(
        'quotes/',
        QuotesAPIViewSet.as_view({
            'get': 'retrieve',
            'post': 'create'
        }),
        name='quotes'
    ),
]
