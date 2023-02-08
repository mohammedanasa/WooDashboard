from accounts import views as account_views
from restaurant import views as restaurant_views
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


restaurant_urlpatterns = [

    path('loc/', restaurant_views.restaurant_list, name="locations"),


    path('categories/', restaurant_views.CategoryList.as_view(), name='categories'),
    path('category/', restaurant_views.create_or_update_category, name='create-category'),
    path('category/<cid>/', restaurant_views.create_or_update_category, name='update-category'),
    path('category/delete-category/<slug:cid>/', restaurant_views.delete_category, name='delete-category'),


    path('product/', restaurant_views.create_or_update_product, name='create-product'),
    path('products/', restaurant_views.ProductList.as_view(), name='products'),
    path('product/<slug:pid>/', restaurant_views.create_or_update_product, name='update-product'),
    path('product/delete-product/<slug:pid>/', restaurant_views.delete_product, name='delete-product'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', account_views.home, name="home"),

    path('login/', account_views.signin, name="login"),
    path('register/', account_views.signup, name="register"),
    path('logout/',account_views.logout_view, name="logout"),

    path('restaurant/',include((restaurant_urlpatterns,'restaurant'))),



    #-------------------Test------------------#
    path('woo/',restaurant_views.fetch_products, name="logout"),
    path('woo1/',restaurant_views.fetch_product_test, name="logout"),




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


