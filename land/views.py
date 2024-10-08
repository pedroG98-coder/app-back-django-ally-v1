from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
)
from land import serializers, models, helpers
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from land.serializers import MyTokenObtainPairSerializer
from django.http import JsonResponse




def index(request):
    return render(request, "land/index.html")



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ==========================================================================================================================
# Vista Lista Para Modelo Usuario
# ==========================================================================================================================


class UsuarioLista(APIView, LimitOffsetPagination):
    permission_classes = [AllowAny]

    def get(self, request):
        objects = models.User.objects.filter(estatus_sistema=True)
        results = self.paginate_queryset(objects, request, view=self)
        serializer = serializers.UserDepthSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        email = request.data.get("email")
        if models.User.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo electrónico ya está en uso"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if password != confirm_password:
            return Response(
                {"error": "Las contraseñas no coinciden"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            pwrd = make_password(password)
            serializer.validated_data["password"] = pwrd
            serializer.save()
            user = models.User.objects.get(id=serializer.data.get("id"))
            user.password = pwrd
            user.is_active = True
            user.save()
            return Response(
                serializers.UserDepthSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ==========================================================================================================================
# Vista Detalle Para Modelo Usuario
# ==========================================================================================================================


class UsuarioDetalle(APIView):

    permission_classes = [AllowAny]

    def get_object(self, pk):
        model_object = get_object_or_404(models.User, pk=pk)
        return model_object

    def get(self, request, pk):
        model_object = self.get_object(pk)
        serializer = serializers.UserDepthSerializer(model_object)
        return Response(serializer.data)

    def put(self, request, pk):
        model_object = self.get_object(pk)
        serializer = serializers.UserSerializer(model_object, data=request.data)
        password = request.data.get("password")
        if serializer.is_valid():
            if password is not None:
                pwrd = make_password(password)
                serializer.password = pwrd
                serializer.save()
                id_user = serializer.data.get("id")
                user = models.User.objects.get(id=id_user)
                user.password = pwrd
                user.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        model_object = self.get_object(pk)
        model_object.estatus_sistema = False
        model_object.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================================================================================================
# Vista Lista Para Modelo Tarea
# ==========================================================================================================================


class TareaLista(APIView, LimitOffsetPagination):
    """
    -Get retorna todos los registros en la bd con estatus en sistema = True
    -Post permite crear un nuevo registro en la base de datos
    """

    permission_classes = [AllowAny]

    def get(self, request):
        objects = models.Tarea.objects.filter(estatus_sistema=True)
        results = self.paginate_queryset(objects, request, view=self)
        serializer = serializers.TareaDepthSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = serializers.TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================================================================
# Vista Detalle Para Modelo Usuario
# ==========================================================================================================================


class TareaDetalle(APIView):

    permission_classes = [AllowAny]

    def get_object(self, pk):
        objeto = get_object_or_404(models.Tarea, pk=pk)
        return objeto

    def get(self, request, pk):
        objeto = self.get_object(pk)
        serializer = serializers.TareaDepthSerializer(objeto)
        return Response(serializer.data)

    def put(self, request, pk):
        model_object = self.get_object(pk)
        serializer = serializers.TareaSerializer(
            model_object, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        objeto = self.get_object(pk)
        objeto.estatus_sistema = False
        objeto.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================================================================================================================
# Vista Metodo Tiempo Restante Tarea
# ==========================================================================================================================

class GETTiempoRestante(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tarea_id):
        try:
            tarea = models.Tarea.objects.get(id=tarea_id)
            tiempo_restante = helpers.get_tiempo_restante(tarea)
            return JsonResponse({"tiempo_restante": tiempo_restante})
        except models.Tarea.DoesNotExist:
            return JsonResponse({"error": "Tarea no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)