from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    role = serializers.SerializerMethodField('get_role')

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'image', 'role']
        read_only_fields = ['id', 'is_admin', 'is_lecturer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            image=None
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if validated_data.get('password'):
            instance.set_password(raw_password=validated_data.get('password'))
        instance.save()
        return instance

    def get_image(self, instance):
        if instance.image:
            return 'http://' + self.context.get('host') + '/media/' + str(instance.image)
        return None

    def get_role(self, instance):
        if instance.is_admin:
            return 2
        elif instance.is_lecturer:
            return 1
        else:
            return 0
