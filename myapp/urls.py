"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from  .import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shp_rgstr/",views.shp_rgstr),
    path("shp_rgstr_post/",views.shp_rgstr_post),
    path("login/",views.login_get),
    path("login_post/",views.login_post),
    path("logout/",views.all_logout),
    path("admin_home/",views.admin_home),
    path("contractor_home/",views.contractor_home),
    path("shop_home/",views.shop_home),
    path("user_home/",views.user_home),
    path("cntrctr_rgstr/",views.cntrctr_rgstr),
    path("cntrctr_rgstr_post/",views.cntrctr_rgstr_post),
    path("verify_shop/",views.verify_shop),
    path("uname_vldtn/",views.username_validation),
    path("shop_accept/<id>",views.shop_accept),
    path("shop_reject/<id>",views.shop_reject),
    path("verify_contractor/",views.verify_contractor),
    path("contractor_accept/<id>",views.contractor_accept),
    path("contractor_reject/<id>",views.contractor_reject),
    path("add_category/",views.add_category),
    path("add_category_post/",views.add_category_post),
    path("view_category/",views.view_category),
    path("delete_category/<id>",views.delete_category),
    path("add_shop_product/",views.add_shop_product),
    path("add_shop_product_post/",views.add_shop_product_post),
    path("edit_shop_product/<id>",views.edit_shop_product),
    path("edit_shop_product_post/",views.edit_shop_product_post),
    path("delete_shop_product/<id>",views.delete_shop_product),
    path("view_shop_product/",views.view_shop_product),
    path("add_offer_product/<id>",views.add_offer_product),
    path("add_offer_product_post/",views.add_offer_product_post),
    path("view_offer_product/",views.view_offer_product),
    path("edit_offer_product/<id>",views.edit_offer_product),
    path("edit_offer_product_post/",views.edit_offer_product_post),
    path("delete_offer_product/<id>",views.delete_offer_product),
    path("view_product/",views.view_product),
    path("contractor_view_product/",views.contractor_view_product),
    path("view_offer/<id>",views.view_offer),
    path("add_contractor_work/",views.add_contractor_work),
    path("add_contractor_work_post/",views.add_contractor_work_post),
    path("view_contractor_work/",views.view_contractor_work),
    path("delete_contractor_work/<id>",views.delete_contractor_work),
    path("edit_contractor_work/<id>",views.edit_contractor_work),
    path("edit_contractor_work_post/",views.edit_contractor_work_post),
    path("user_login/",views.user_login),
    path("user_login_post/",views.user_login_post),
    path("user_rgstr/",views.user_register),
    path("user_rgstr_post/",views.user_register_post),
    path("home/",views.home),
    path("cart/<id>",views.cart),
    path("cart_post/",views.cart_post),
    path("view_cart/",views.view_cart),
    path("remove_cart/<id>",views.remove_cart),
    path("raz_pay/", views.raz_pay, name="raz_pay"),
    # path("send_rating/",views.send_rating),
    # path("send_rating_post/",views.send_rating_post),
    path("view_contractors/",views.view_contractors),
    path("view_work/<id>",views.view_work),
    path("send_feedback/",views.send_feedback),
    path("send_feedback_post/",views.send_feedback_post),
    path("send_complaint/",views.send_complaint),
    path("send_complaint_post/",views.send_complaint_post),
    path("view_rating/",views.view_feedback_review),
    path("view_order_main/",views.view_order_main),
    path("view_order_sub/<id>",views.view_order_sub),
    path("view_shop_order/",views.view_shop_orders),
    path("view_shop_order_sub/<id>",views.view_shop_order_sub),
    path("order_confirm/<id>",views.order_confirm),
    path("order_reject/<id>",views.order_reject),
    path("view_feedback/",views.view_feedback),
    path("view_complaint/",views.view_complaints),
    path("send_reply/<id>",views.send_reply),
    path("send_reply_post/",views.send_reply_post),
    path("view_reply/",views.view_reply),
    path("send_work_request/<id>",views.send_work_request),
    path("view_work_request/",views.view_work_request),
    path("work_request_accept/<id>",views.work_request_accept),
    path("work_request_reject/<id>",views.work_request_reject),
    path("user_view_request_status/<id>",views.user_view_request_status),










]
