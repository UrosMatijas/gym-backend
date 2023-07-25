ENDPOINTS FOR GYM BACKEND:

1. register/ [POST]<-- Register new user. (Required: username, gender, email, password, address, mobile)
2. login/ [POST]<-- Login user.
3. logout/ [POST]<-- Logout user.

4. users/ [GET]{admin}<-- List all users

5. manage_profile/ [GET, PUT]<-- Manage profile information.

6. manage/<int:pk>/ [GET, PUT, DELETE]{admin} <-- Manage user(pk). GET user info, update user type(giving trainer 
                                                 permission) or delete user.
7. manage/trainers/<int:pk>/ [GET, PUT]{admin}<-- Manage trainers(pk). GET trainer info, update trainer info(salary
                                                   and details)

8. feedbacks/ [GET, POST] <-- GET all the feedbacks or create one (required: details, rating).
9. feedback/<int:pk>/ [GET, PUT, DELETE] <-- GET single feedback, update feedback(required: details, rating), 
                                             delete feedback.

10. plans/ [GET]<-- GET all workout plans.

11. membership/<int:pk>/ [GET] <-- GET membership of user(pk).
12. memberships/ [GET, POST] <-- GET all the memberships or create one(plan_id required).
13. update_membership/<int:pk>/ [PUT] <-- Update plan info on membership(pk), plan_id required.
14. manage_membership/<int:pk>/ [PUT]{admin} <-- Update membership status(status should be Active or Inactive). 

15. attendance/<int:pk>/ [GET, POST]<--GET all attendances from user(pk). Create attendance(admin or trainer only).
16. attendances/ [GET] <-- GET all attendances.

17. orders/ [GET, POST] <-- GET all products. Order product(required: product_id, quantity)
18. manage_orders/<int:pk>/ [PUT]{admin} <-- Update delivery status(status should be Ongoing or Finished)

