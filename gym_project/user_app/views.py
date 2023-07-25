from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        type_id = 3
        username = request.data.get('username')
        gender = request.data.get('gender')
        email = request.data.get('email')
        password = request.data.get('password')
        address = request.data.get('address')
        mobile = request.data.get('mobile')

        if not username or not password or not gender or not email or not address or not mobile:
            return Response({'error': 'Please provide all the information: username, gender, email,'
                                      ' password, address and mobile.'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists. Please choose a different username.'}, status=400)

        new_user = User.objects.create_user(username=username, password=password)
        if new_user:
            with connection.cursor() as cursor:
                cursor.execute("""
                                INSERT INTO user_master 
                                (
                                user_id, 
                                type_id, 
                                user_name, 
                                gender, 
                                email, 
                                password, 
                                address, 
                                mobile
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s )
                                """,
                                [new_user.id, type_id, username, gender, email, new_user.password, address, mobile])
                connection.commit()

        return Response({'message': 'Registration successful.'}, status=201)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return Response({'message': 'Logout first.'}, status=400)

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful.'}, status=200)
        else:
            return Response({'error': 'Invalid username or password.'}, status=401)

@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful.'}, status=200)

@login_required
@api_view(['GET', 'PUT'])
def manage_profile(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            user_id = request.user.id
            cursor.execute("""
                        SELECT *
                        FROM user_master
                        WHERE user_id_id = %s
                        """,
                        [user_id])
            user_data = cursor.fetchone()

            if user_data:
                columns = [col[0] for col in cursor.description]
                user_dict = dict(zip(columns, user_data))
                return Response({'user': user_dict}, status=200)
            else:
                return Response({'error': 'Profile data not returned.'}, status=400)

    if request.method == 'PUT':
        fields_to_update = {}
        update_query = "UPDATE user_master SET "

        if 'user_name' in request.data:
            fields_to_update['user_name'] = request.data['user_name']
        if 'gender' in request.data:
            fields_to_update['gender'] = request.data['gender']
        if 'email' in request.data:
            fields_to_update['email'] = request.data['email']
        if 'password' in request.data:
            fields_to_update['password'] = request.data['password']
        if 'address' in request.data:
            fields_to_update['address'] = request.data['address']
        if 'mobile' in request.data:
            fields_to_update['mobile'] = request.data['mobile']

        update_values = []
        for field, value in fields_to_update.items():
            update_query += f"{field} = %s, "
            update_values.append(value)
        update_query = update_query.rstrip(', ')
        update_query += " WHERE user_id_id = %s"
        update_values.append(request.user.id)

        with connection.cursor() as cursor:
            cursor.execute(update_query, update_values)
            connection.commit()

        return Response({'message': 'Profile updated successfully.'}, status=200)

@permission_classes([IsAdminUser])
@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT *
                        FROM user_master
                        """)

            user_data = cursor.fetchall()

            if user_data:
                columns = [col[0] for col in cursor.description]
                user_dict = dict(zip(columns, user_data))

                return Response({'users': user_dict}, status=200)
            else:
                return Response({'error': 'No users found'}, status=404)

@permission_classes([IsAdminUser])
@api_view(['GET', 'PUT', 'DELETE'])
def manage_users(request, pk):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT * FROM user_master
                            WHERE user_id=%s
                            """,
                            [pk])
                user_data = cursor.fetchone()

            if user_data:
                columns = [col[0] for col in cursor.description]
                user_dict = dict(zip(columns, user_data))

                return Response({'user': user_dict}, status=200)
        except:
            return Response({'error': 'Wrong user id.'}, status=400)

    if request.method == 'PUT':
        type_id = request.data.get('type_id')

        if not pk or not type_id:
            return Response({'error': 'Please provide both user_id(endpoint) and type_id.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                        UPDATE user_master
                        SET type_id = %s 
                        WHERE user_id = %s
                        """,
                        [type_id, pk])
            connection.commit()

        if type_id == 2:
            with cursor.cursor() as cursor:
                cursor.execute("""
                            INSERT INTO trainer_details (
                            user_id_id
                            ) VALUES (%s)
                            """,
                            [pk])
                connection.commit()
                rows_updated = cursor.rowcount

        if rows_updated > 0:
            return Response({'message': 'User type updated successfully.'}, status=200)
        else:
            return Response({'error': 'User type not updated.'}, status=404)

    if request.method == 'DELETE':
        if not pk:
            return Response({'error': 'Add pk endpoint to delete.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                        DELETE FROM user_master
                        WHERE user_id = %s
                        """,
                        [pk])
            connection.commit()

            rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            return Response({'message': 'User deleted successfully.'}, status=200)
        else:
            return Response({'error': 'User not found.'}, status=404)

@permission_classes([IsAdminUser])
@api_view(['GET', 'PUT'])
def manage_trainers(request, pk):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT * 
                        FROM trainer_details
                        WHERE trainer_id=%s
                        """,
                        [pk])
                trainer_data = cursor.fetchone()

            if trainer_data:
                columns = [col[0] for col in cursor.description]
                trainer = dict(zip(columns, trainer_data))

                return Response({'trainer': trainer}, status=200)
        except:
            pass

        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT *
                    FROM trainer_details
                    """)

            columns = [col[0] for col in cursor.description]
            trainers = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response({'trainers': trainers}, status=200)

    if request.method == 'PUT':
        salary = request.data.get('salary')
        details = request.data.get('details')

        if not pk:
            return Response({'error': 'Please provide trainer_id(endpoint).'}, status=400)

        if salary and details:
            with connection.cursor() as cursor:
                cursor.execute("""
                            UPDATE trainer_details
                            SET salary = %s, details = %s 
                            WHERE trainer_id = %s
                            """,
                            [salary, details, pk])
                connection.commit()

                rows_updated = cursor.rowcount
        else:
            return Response({'error': 'Provide both salary and details.'}, status=400)

        if rows_updated > 0:
            return Response({'message': 'Trainer info updated successfully.'}, status=200)
        else:
            return Response({'error': 'Trainer not found.'}, status=404)






