from . import models
from cmdb.models import User,Resources,UserLikes,UserComment
from cmdb.serializers import UserSerializer,ResourceSerializer,UserCreateSerializer,UserDetailSerializer,CommentSerializer,CommentCreateSerializer,NewCommentSerializer, \
    ResourceDisplaySerializer
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password


class UserView(APIView):
    # 列出所有
    def get(self, request, format=None):
        user=models.User.objects.all()
        serializer= UserSerializer(user, many=True)
        return Response(serializer.data)
    # 新建一个
    def post(self, request, format=None):
        import time
        request.data['created_at']=int(time.time())
        request.data['updated_at']=int(time.time())
        request.data['password'] = make_password(request.data['password'])
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_vaild():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            raise Http404
    # 读取
    def get(self, request, pk, frmat=None):
        user = self.get_object(pk)
        serializer= UserDetailSerializer(user)
        return Response(serializer.data)


    # def put(self, request, pk, format=None):
    # 	user = self.get_object(pk)
    # 	serializer = SnippetSerializer(user, data=request.data)
    # 	if serializer.is_valid():
    # 		serializer.save()
    # 		return Response(serializer.data)
    # 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceList(APIView):
    def get(self, request):
        resources = models.Resources.objects.all().order_by('-created_at')
        serializer = ResourceDisplaySerializer(resources, many=True)
        return Response(serializer.data)

    def get_(self, request, format=None):
        uid = request.GET.get("user_id")
        resource = models.Resources.objects.all().order_by("-created_at")
        serializer = ResourceSerializer(resource, many=True)
        # serializer.data['nickname']=user.nickname
        # return Response(serializer.data)
        nickname_list=[]
        for x in resource:
            nickname_list.append(x.user.nickname)

        result=[]
        num=0
        import time
        for item in serializer.data:
            item['nickname'] = nickname_list[num]
            item['praise_num'] = models.UserLikes.objects.filter(resources_id=item['id']).count()
            comment_data = models.UserComment.objects.filter(resources_id = item['id'])
            comment_serializer = CommentSerializer(comment_data,many=True)
            item['comment'] = comment_serializer.data

            # now_time = time.localtime(time.time())
            # if (now_time[0]-int(item['created_at'])>0):
            # 	print ('ok')
            now_time = int(time.time())
            time_diff_seconds = now_time - item['created_at']
            time_diff_day = int(time_diff_seconds / 60 / 60 / 24)
            time_diff_hours = int(time_diff_seconds / 60 / 60)
            time_diff_minutes = int(time_diff_seconds / 60)

            if (time_diff_day > 0):
                item['time_diff'] = str(time_diff_day) + ' 天'
            elif (time_diff_hours > 0):
                item['time_diff'] = str(time_diff_hours) + ' 时'
            elif (time_diff_minutes > 0):
                item['time_diff'] = str(time_diff_minutes) + ' 分'
            else:
                item['time_diff'] = str(time_diff_seconds) + ' 秒'

            del item['user']
            result.append(item)
            num += 1

        # result.pop(user)
        return Response(result)

    def post(self,request,format=None):
        serializer = ResourceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print(serializer.validated_data)
        resource = serializer.save()

        # new_resource = Resources(**serializer.validated_data)
        # print(new_resource)
        # new_resource.save()
        return Response('ok')
        # serializer = ResourceSerializer(data=request.data)
        # if serializer.is_valid():
        # 	serializer.save()
        # 	return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    def get(self, request,format=None):
        comment= models.UserComment.objects.all()
        serializer = NewCommentSerializer(comment,many=True)
        return Response(serializer.data)

    def post(self, request,format=None):
        import time
        request.data['created_at']=int(time.time())
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


