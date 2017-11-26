from rest_framework import serializers

from cmdb.models import Resources, User
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','email','nickname','prefix','phone','created_at','updated_at')


class ResourceDisplaySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.pk')
    nickname = serializers.CharField(source='user.nickname')
    time_diff = serializers.CharField()
    praise_num = serializers.IntegerField(source='likes.count')

    class Meta:
        model = models.Resources
        exclude = ['user']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resources
        fields = ('id', 'user', 'title','img_url', 'created_at','updated_at')
        extra_kwargs = {
            'user_id': {'write_only': True}
        }

    def create(self, validated_data):
        resource = models.Resources(**validated_data)
        author = User.objects.get(pk=validated_data['user_id'])
        resource.user = author
        resource.save()
        return resource


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','password','email','nickname','prefix','phone','created_at','updated_at')



class UserDetailSerializer(serializers.ModelSerializer):
    resources_set = ResourceSerializer(many=True, read_only=True)
    class Meta:
        model = models.User
        fields = ('id','email','nickname','prefix','phone','created_at','updated_at','resources_set')

class CcSerializer(serializers.RelatedField):
    def to_representation(self,value):
        result = {}
        result['email'] = value.email
        result['nickname'] = value.nickname
        result['phone'] = value.phone
        result['created_at'] = value.created_at
        return result


class CommentSerializer(serializers.ModelSerializer):
    user = CcSerializer(read_only=True)
    class Meta:
        model = models.UserComment
        fields = ('user_id','content','created_at','user')
        depth = 1

class NewCommentSerializer(serializers.ModelSerializer):
    user = CcSerializer(read_only=True)
    class Meta:
        model = models.UserComment
        fields = ('id','user_id','resources_id','content','created_at','user')
        depth = 1

# 评论插入
class CommentCreateSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    # resources_id = serializers.IntegerField()
    class Meta:
        model = models.UserComment
        fields = ('id','user_id', 'resources_id', 'content', 'created_at')