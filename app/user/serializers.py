"""
Serializers for the user API view.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.utils.translation import gettext as _

from rest_framework import  serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ['email','password','first_name','last_name','username']
        extra_kwargs = {'password':{'write_only':True, 'min_length': 5}}

    ##over-ride the create method so the password shold he hashed.
    def create(self, validated_data):
        """Create and return a user with encypted password"""
        return User.objects.create_user(**validated_data)

    ##password should be hashed
    def update(self, instance, validated_data):
        """Update and return user"""
        #update everything except for password
        password = validated_data.pop('password', None)  # None as password is optional when updating, pop as we do not want to leave the password in there
        user = super().update(instance, validated_data) # no need to re-wirte update method so call of superclass

        if password: # if password was set
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace=False,
    )
    username = serializers.CharField(
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        user = authenticate(
            request = self.context.get('request'), #required field
            username = username,
            email=email,
            password = password,
        )

        if not user:
                msg = _('Unable to authenticate with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization') # translated to http 400 bad request

        attrs['user']  = user # set the user attribute , view expects that to be set then the authenticalion is valid
        return attrs



