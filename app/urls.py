from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .form import UserLoginForm, UserChangePasswordForm, mypasswordReset, mypasswordConform

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('add_to_checkout/', views.add_to_checkout, name='add_to_checkout'),
    path('cart/', views.show_cart, name='show_cart'),
    # my logic :
    # path('addqut/<int:id>', views.Add_Quntity, name="addqut"),
    # path('minesqut/<int:id>', views.Mines_Quntity, name="minesqut"),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('remove/<int:id>', views.remove_cart, name='remove'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobilelist'),
    
    path('registration/', views.customerregistration, name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=UserChangePasswordForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passchangedone.html'), name='passwordchangedone'),
   
    path('passwordreset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html' , form_class=mypasswordReset), name='passwordreset' ),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done' ),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=mypasswordConform), name='password_reset_confirm' ),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete' ),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
