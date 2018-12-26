from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from rest_api.models.Training import Training, Stage, Contest
from rest_api.serializers.TrainingSerializer import TrainingListSerializer, TrainingCreateSerializer, \
    StageListSerializer, TrainingStageSerializer, StageContestSerializer


class TrainingView(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    # lookup_field = "username"
    # serializer_class = TrainingSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrainingCreateSerializer
        return TrainingListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(create_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class StageView(viewsets.ModelViewSet):
#     queryset = Stage.objects.all()
#     # lookup_field = "username"
#     # serializer_class = TrainingSerializer
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return StageListSerializer
#         return StageDetailSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(create_user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class TrainingStageView(viewsets.ModelViewSet):
    def get_queryset(self):
        return Stage.objects.filter(training_id=self.kwargs['training_pk'])
    
    def get_serializer_class(self):
        return TrainingStageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(create_user=request.user, training_id=self.kwargs['training_pk'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StageContestView(viewsets.ModelViewSet):
    def get_queryset(self):
        return Contest.objects.filter(stage_id=self.kwargs['stage_pk'])

    def get_serializer_class(self):
        return StageContestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(create_user=request.user, stage_id=self.kwargs['stage_pk'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#
# class ManagerView(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserManagerSerializer
