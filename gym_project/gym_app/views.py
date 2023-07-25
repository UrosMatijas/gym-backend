from django.contrib.auth.decorators import login_required
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import date

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def feedback(request, pk):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT * FROM feedback_master
                        WHERE feedback_id=%s
                        """,
                        [pk])
                feedback_data = cursor.fetchone()

            if feedback_data:
                columns = [col[0] for col in cursor.description]
                feedback_dict = dict(zip(columns, feedback_data))

                return Response({'feedback': feedback_dict}, status=200)
        except:
            pass
        return Response({'error': 'Cant find feedback info.'}, status=400)

    if request.method == 'PUT':
        details = request.POST.get('details')
        rating = request.POST.get('rating')

        if not details or not rating:
            return Response({'error': 'Please provide both details and rating.'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT user_id_id 
                        FROM feedback_master 
                        WHERE feedback_id=%s
                        """,
                        [pk])
                feedback_data = cursor.fetchone()

                if feedback_data and feedback_data[0] == request.user.id:
                    cursor.execute("""
                            UPDATE feedback_master
                            SET comment=%s, rating=%s
                            WHERE feedback_id=%s
                            """,
                            [details, rating, pk])

                    connection.commit()
                    return Response({'message': 'Feedback updated successfully.'}, status=200)
                else:
                    return Response({'error': 'You are not authorized to update this feedback.'}, status=403)

        except:
            return Response({'error': 'Error updating the feedback. Please try again.'}, status=500)

    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT user_id 
                        FROM feedback_master 
                        WHERE feedback_id=%s
                        """,
                        [pk])
                feedback_data = cursor.fetchone()

                if feedback_data and feedback_data[0] == request.user.id:
                    cursor.execute("""
                            DELETE FROM feedback_master 
                            WHERE feedback_id=%s
                            """,
                            [pk])

                    connection.commit()
                    return Response({'message': 'Feedback deleted successfully.'}, status=200)
                else:
                    return Response({'error': 'You are not authorized to delete this feedback.'}, status=403)

        except:
            return Response({'error': 'Error deleting the feedback. Please try again.'}, status=500)

@login_required
@api_view(['GET', 'POST'])
def feedbacks(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT *
                    FROM feedback_master
                    """)
            columns = [col[0] for col in cursor.description]
            feedbacks = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response({'feedbacks': feedbacks}, status=200)

    if request.method == 'POST':
        details = request.data.get('details')
        rating = request.data.get('rating')

        if not details or not rating:
            return Response({'error': 'Please provide both comment and rating.'}, status=400)
        elif rating < 1 or rating > 5:
            return Response({'error': 'Rating must be between 1 and 5.'}, status=400)

        user_id = request.user.id
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT * FROM feedback_master
                            WHERE user_id_id = %s
                            """,
                            [user_id])

                if not cursor.fetchone():
                    cursor.execute("""
                                INSERT INTO feedback_master (
                                details, 
                                rating,
                                user_id_id,
                                )
                                VALUES (%s, %s)
                                """,
                                [details, rating, user_id])
                    connection.commit()
                else:
                    return Response({'error': 'You have already submitted feedback.'}, status=400)

        except:
            return Response({'error': 'Feedback not submitted.'}, status=400)
        return Response({'message': 'Feedback added successfully.'}, status=201)

@login_required
@api_view(['GET'])
def plans(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT *
                    FROM plan_master
                    """)
        columns = [col[0] for col in cursor.description]
        plans = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return Response({'plans': plans}, status=200)

@login_required
@api_view(['GET'])
def membership(request, pk):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT *
                            FROM membership_master
                            WHERE user_id_id = %s
                            """,
                            [pk])
                membership_data = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            memberships = [dict(zip(columns, row)) for row in membership_data]

            if memberships:
                return Response({'memberships': memberships}, status=200)
            else:
                return Response({'error': 'Membership not found.'}, status=404)

        except:
            return Response({'error': 'Error fetching membership data.'}, status=500)

@login_required
@api_view(['GET', 'POST'])
def memberships(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT *
                            FROM membership_master
                            """)

                membership_data = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            memberships = [dict(zip(columns, row)) for row in membership_data]

            if memberships:
                return Response({'memberships': memberships}, status=200)
            else:
                return Response({'error': 'Membership not found.'}, status=404)

        except:
            return Response({'error': 'Error fetching membership data.'}, status=500)

    if request.method == 'POST':
        user_id = request.user.id
        plan_id = request.data.get('plan_id')

        if not plan_id:
            return Response({'error': 'Please provide a plan_id.'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT *
                        FROM plan_master
                        WHERE plan_id = %s
                        """,
                        [plan_id])

                plan_data = cursor.fetchone()

                if not plan_data:
                    return Response({'error': 'Invalid plan_id. Plan not found.'}, status=404)

                cursor.execute("""
                            SELECT *
                            FROM membership_master
                            WHERE user_id_id=%s
                            """,
                            [user_id])
                memb_data = cursor.fetchone()

                if memb_data is None:
                    start_date = date.today()
                    status = 'Pending'
                    cursor.execute("""
                            INSERT INTO membership_master (
                            user_id_id, 
                            plan_id_id,
                            start_date,
                            status
                            )
                            VALUES (%s, %s)
                            """,
                            [user_id, plan_id, start_date, status])
                    connection.commit()
                else:
                    return Response({'error': 'User already has a membership.'}, status=401)

        except:
            return Response({'error': 'Error creating membership.'}, status=500)

        membership_id = cursor.lastrowid

        return Response({
            'membership': {
                'membership_id': membership_id,
                'user_id': user_id,
                'plan': {
                    'plan_id': plan_data[0],
                    'title': plan_data[1],
                    'details': plan_data[2],
                    'price': plan_data[3],
                    'duration': plan_data[4],
                },
                'start_date': start_date.isoformat(),
            },
            'message': 'Membership created successfully.',
        }, status=201)

@login_required
@api_view(['PUT'])
def update_membership(request, membership_id):
    if request.method == 'PUT':
        user_id = request.user.id
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT *
                        FROM membership_master
                        WHERE membership_id = %s
                        AND user_id_id = %s
                        """,
                        [membership_id, user_id])

                membership_data = cursor.fetchone()

                if not membership_data:
                    return Response({'error': 'Membership not found or not authorized.'}, status=404)

                plan_id = request.data.get('plan_id')
                if plan_id:
                    cursor.execute("""
                            SELECT *
                            FROM plan_master
                            WHERE plan_id = %s
                            """,
                            [plan_id])

                    plan_data = cursor.fetchone()

                    if not plan_data:
                        return Response({'error': 'Invalid plan_id. Plan not found.'}, status=404)

                    cursor.execute("""
                            UPDATE membership_master
                            SET plan_id_id = %s
                            WHERE membership_id = %s
                            """,
                            [plan_id, membership_id])

                connection.commit()

        except:
            return Response({'error': 'Error updating membership.'}, status=500)

        return Response({'message': 'Membership updated successfully.'}, status=200)

@permission_classes([IsAdminUser])
@api_view(['PUT'])
def manage_membership(request, membership_id):
    if request.method == 'PUT':
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT *
                        FROM membership_master
                        WHERE membership_id = %s
                        AND status = 'Pending' 
                        """,
                        [membership_id])
            memb_data = cursor.fetchall()

            if memb_data:
                status = request.data.get('status')
                if status != 'Active' and status != 'Inactive':
                    return Response({'error': 'Status should be Active or Inactive.'}, status=400)
                else:
                    cursor.execute("""
                                UPDATE membership_master
                                SET status = %s
                                WHERE membership_id = %s
                                """,
                                [status, membership_id])
                    connection.commit()
                    return Response({'success': 'Membership status updated.'}, status=200)
            else:
                return Response({'error': 'Invalid membership.'}, status=400)

@login_required
@api_view(['GET'])
def attendances(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT *
                        FROM attendance_master
                        """)

            attendance_data = cursor.fetchall()

            if attendance_data:
                columns = [col[0] for col in cursor.description]
                attendances = [dict(zip(columns, row)) for row in attendance_data]
                return Response({'attendances': attendances}, status=200)
            else:
                return Response({'error': 'Cant find attendance data.'}, status=400)

@login_required
@api_view(['GET', 'POST'])
def attendance(request, pk):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT *
                    FROM attendance_master
                    WHERE user_id_id = %s
                    """,
                    [pk])

            attendance_data = cursor.fetchall()

            if attendance_data:
                columns = [col[0] for col in cursor.description]
                attendances = [dict(zip(columns, row)) for row in attendance_data]
                return Response({'attendances': attendances}, status=200)
            else:
                return Response({'error': 'No attendance records found.'}, status=404)

    if request.method == 'POST':
        if request.user.id == 2 or request.user.is_admin:
            with connection.cursor() as cursor:
                att_date = date.today()
                cursor.execute("""
                            INSERT INTO attendance_master (
                            user_id_id,
                            attendance_date
                            )
                            VALUES (%s, %s)
                            """,
                            [pk, att_date])
                connection.commit()

                attendance_id = cursor.lastrowid

                cursor.execute("""
                            SELECT *
                            FROM attendance_master
                            WHERE attendance_id = %s
                            """,
                            [attendance_id])

                attendance_data = cursor.fetchone()
                if attendance_data:
                    columns = [col[0] for col in cursor.description]
                    attendance = dict(zip(columns, attendance_data))
                    return Response({'attendance': attendance}, status=200)
                else:
                    return Response({'error': 'Failed to fetch attendance record.'}, status=500)

@login_required
@api_view(['GET', 'POST'])
def order_products(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT *
                        FROM product_master
                        """)
            products_data = cursor.fetchall()

            if products_data:
                columns = [col[0] for col in cursor.description]
                products = [dict(zip(columns, row)) for row in products_data]
                return Response({'products': products}, status=200)
            else:
                return Response({'error': 'No product records found.'}, status=404)

    if request.method == 'POST':
        user_id = request.user.id
        order_date = date.today()
        delivery_status = 'Pending'

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({'error': 'Please provide the product_id.'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT * FROM product_master 
                            WHERE product_id = %s
                            """,
                            [product_id])
                product_data = cursor.fetchone()

                if not product_data:
                    return Response({'error': 'Invalid product_id. Product not found.'}, status=404)

                available_quantity = product_data['quantity']
                if quantity > available_quantity:
                    return Response({'error': 'Insufficient quantity in stock.'}, status=400)

                price = product_data['price']
                total_amount = quantity * price

                cursor.execute("""
                            INSERT INTO order_master (
                            user_id_id, 
                            order_date,
                            delivery_status)
                            VALUES (%s, %s, %s)
                            """,
                            [user_id, order_date, delivery_status])

                order_id = cursor.lastrowid

                cursor.execute("""
                            INSERT INTO order_details (
                            order_id_id, 
                            product_id_id, 
                            quantity, 
                            price, 
                            total_amount)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            [order_id, product_id, quantity, price, total_amount])

                cursor.execute("""
                            UPDATE product_master
                            SET quantity = quantity - %s
                            WHERE product_id = %s
                            """,
                            [quantity, product_id])

                connection.commit()

                return Response({'message': 'Order created successfully.'}, status=201)

        except:
            return Response({'error': 'Error creating the order. Please try again.'}, status=500)

@permission_classes([IsAdminUser])
@api_view(['PUT'])
def manage_order(request, order_id):
    if request.method == 'PUT':
        with connection.cursor() as cursor:
            try:
                delivery_status = request.data.get('status')
                if delivery_status != 'Ongoing' or delivery_status != 'Finished':
                    return Response({'error': 'Order status should be Ongoing or Finished.'}, status=400)

                cursor.execute("""
                            UPDATE order_master
                            SET delivery_status = %s
                            where order_id = %s
                            """,
                            [delivery_status, order_id])
                connection.commit()
                return Response({'success': 'Order status updated successfully.'}, status=200)

            except:
                return Response({'error': 'Order status update failed'}, status=400)














