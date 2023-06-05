from rest_framework import serializers
from .models import Question, Answer
from .custom_relational_fields import UsernameEmailRelationalField


class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    email = serializers.EmailField()


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField(method_name='all_answers')
    user = UsernameEmailRelationalField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def all_answers(self, obj):
        queryset = obj.answers.all()
        return AnswerSerializer(instance=queryset, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

