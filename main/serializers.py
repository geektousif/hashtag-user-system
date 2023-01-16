from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        fields = ('id', 'name', 'email', 'date_of_birth',
                  'bio', 'password', 'password2')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            if password != password2:
                raise serializers.ValidationError(
                    {'password': 'Passwords must match.'})
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                if validated_data['password'] != validated_data['password2']:
                    raise serializers.ValidationError(
                        {'password': 'Passwords must match.'})
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'date_of_birth', 'bio')
