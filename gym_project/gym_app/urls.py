from django.urls import path
from gym_app.views import feedbacks, membership, update_membership, plans, \
                        memberships, attendances, order_products, feedback, attendance, manage_membership, \
                        manage_order



urlpatterns = [
    path('feedbacks/', feedbacks, name='feedback'),
    path('feedback/<int:pk>/', feedback, name='single_feedback'),

    path('plans/', plans, name='plans'),

    path('membership/<int:pk>/', membership, name='membership'),
    path('memberships/', memberships, name='memberships'),
    path('update_membership/<int:pk>/', update_membership, name='update_membership'),
    path('manage_membership/<int:pk>/', manage_membership, name='manage_membership'),

    path('attendance/<int:pk>/', attendance, name='attendance'),
    path('attendances/', attendances, name='attendances'),

    path('orders/', order_products, name='orders'),
    path('manage_orders/<int:pk>/', manage_order, name='manage_order')
]