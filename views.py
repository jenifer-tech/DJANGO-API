from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated	 
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from account.serializers import RegistrationSerializer,AccountPropertiesSerializer
from account.models import Account
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0')
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data,status=status.HTTP_400_BAD_REQUEST)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data,status=status.HTTP_400_BAD_REQUEST)
		serializer = RegistrationSerializer(data=request.data)		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
			return Response(data,status=status.HTTP_201_CREATED)
		else:
			data = serializer.errors
			return Response(data,status=status.HTTP_204_NO_CONTENT)
def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email
def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)		
	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = 'Account update successfully'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class ObtainAuthTokenView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes=[TokenAuthentication]
	def post(self, request):
		context = {}
		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
			return Response(context,status=status.HTTP_202_ACCEPTED)
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'
			return Response(context,status=status.HTTP_401_UNAUTHORIZED)
	