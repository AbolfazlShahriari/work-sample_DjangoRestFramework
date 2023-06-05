from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person, Question, Answer
from .serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializer(persons, many=True)
        return Response(ser_data.data)


class QuestionListView(APIView):# for CRUD
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):# for read
        questions = Question.objects.all()
        ser_data = QuestionSerializer(questions, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def post(self, request):  # for create
        ser_data = QuestionSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, pk):# for update
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        ser_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, pk):# for delete
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'question deleted'})



