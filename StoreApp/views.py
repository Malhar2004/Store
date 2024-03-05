from .models import Customer_info,CustomUser, Draw_date
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .serializers import Customer_serializer, UserSerializer, Draw_date_serializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from openpyxl import Workbook
from rest_framework.views import APIView

# Create your views here.



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if user:
            user = authenticate(username=user.username, password=password)
        else:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
            # response = JsonResponse({'token': token.key})
            # response.set_cookie(key='auth_token', value=token.key,
            #                     httponly=True, path='/')  # Setting the token as an HTTP-only cookie
            # return response

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    user_info = {
        'username': user.username,
        'email' : user.email,
    }
    return Response(user_info)


class CustomerInfo(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Customer_info.objects.all()
    serializer_class = Customer_serializer




@permission_classes([IsAuthenticated])
def export_to_excel(request):
    # Retrieve data from the database via DRF view
    customer_data = Customer_info.objects.all()

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active

    # Write headers
    headers = ['Name', 'Mobile_No', 'Invoice_No', 'Invoice_Date','Amount', 'Coupon_id', 'draw_date']
    ws.append(headers)

    # Write data to Excel
    for customer_row in customer_data:
        formated_invoice_date = customer_row.Invoice_date.strftime("%d-%m-%Y")
        formated_draw_date = customer_row.dr_date.strftime("%d-%m-%Y")
        ws.append([customer_row.Name, customer_row.Mobile_No, customer_row.Invoice_no,formated_invoice_date, customer_row.Amount, customer_row.Token_id,formated_draw_date])

    # Create a response containing the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    wb.save(response)

    return response


class DrawDate(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Draw_date.objects.all()
    serializer_class = Draw_date_serializer
