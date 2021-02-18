from rest_framework import serializers
from rest_framework import status
from account.models import Account
from rest_framework.response import Response
# class LoginSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Account
# 		fields = ['email', 'password',]

# 		extra_kwargs = {'password': {'write_only': True}}

# 	def validate(self, data):
# 		password = data.get('password')
# 		email = data.get('email')
class RegistrationSerializer(serializers.ModelSerializer):
	password2 =  serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}
	def	save(self):
		account = Account(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
			return Response(status=status.HTTP_400_BAD_REQUEST)
		account.set_password(password)
		account.save()
		return account
class AccountPropertiesSerializer(serializers.ModelSerializer):
	class Meta:		
		model = Account
		fields = ['pk','email', 'password']



	
