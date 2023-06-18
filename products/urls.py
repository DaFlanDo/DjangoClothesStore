from django.urls import path

from products.views import IndexView,   ProductListView, basket_add, basket_remove

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(extra_context={'title':'Storedimas'}), name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket/add'),
    path('baskets/remove/<int:baskets_id>/', basket_remove, name='basket/remove'),
    path('category/<int:category_id>/', ProductListView.as_view(),name='category'),
    path('page/<int:page>/',ProductListView.as_view(),name='paginator'),

]

