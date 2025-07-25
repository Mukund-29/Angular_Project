from rest_framework import serializers
from soloapp.models import Unit, Employee
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UnitSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Unit
        fields = ('Unit_Id', 'Unit_Name')

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = Employee
        fields = (
            'NTID',
            'password',
            'First_Name',
            'Last_Name',
            'Email_Id',
            'Unit_Name',
            'IsActive',
            'PhotoFileName',
        )

    def validate_NTID(self, value):
        if Employee.objects.filter(NTID=value).exists():
            raise serializers.ValidationError("NTID already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        ntid = validated_data.pop('NTID')
        email = validated_data.pop('Email_Id')

        if not validated_data.get('PhotoFileName'):
            validated_data['PhotoFileName'] = f"{ntid}.jpg"

        user = Employee.objects.create_user(
            NTID=ntid,
            Email_Id=email,
            password=password,
            **validated_data
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['NTID'] = user.NTID
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'NTID': self.user.NTID,
            'First_Name': self.user.First_Name,
            'Last_Name': self.user.Last_Name,
            'Email_Id': self.user.Email_Id,
            'Unit_Name': self.user.Unit_Name,
            'IsActive': self.user.IsActive,
            'PhotoFileName': self.user.PhotoFileName,
        }
        return data
