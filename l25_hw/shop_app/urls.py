from django.urls import path
from .views import async_home


urlpatterns = [
    path("", async_home, name='home')

    # path("", HomeView.as_view(), name='home'),
    # path("login/", views.LoginView.as_view(), name='login'),
    # path("logout/", views.user_logout, name='logout'),
    #
    # path("user_admin/", views.UserAdminView.as_view(), name='user_admin'),
    # path("search/", views.SearchView.as_view(), name='search'),
    # path("contacts/", views.ContactsView.as_view(), name='contacts'),
    # path("category/<str:category_name>/", views.CategoryView.as_view(), name='category'),
    # path("subcategory/<slug:subcategory>/", views.SubcategoryView.as_view(), name='subcategory'),
    # path("item/<str:item_id>/", views.ItemView.as_view(), name='item'),
    # path("item/<str:item_id>/add/", views.ItemView.as_view(), name='item'),
    # path("basket/", views.BasketView.as_view(), name='basket'),
    # path("complete_purchase/", views.CompletePurchase.as_view(), name='complete_purchase')
]
