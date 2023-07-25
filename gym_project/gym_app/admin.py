from django.contrib import admin
from gym_app.models import FeedbackMaster, MembershipMaster, PlanMaster, PaymentMaster, \
                            AttendanceMaster, ProductMaster, OrderMaster, OrderDetails

admin.site.register(FeedbackMaster)
admin.site.register(PlanMaster)
admin.site.register(PaymentMaster)
admin.site.register(MembershipMaster)
admin.site.register(AttendanceMaster)
admin.site.register(ProductMaster)
admin.site.register(OrderDetails)
admin.site.register(OrderMaster)

