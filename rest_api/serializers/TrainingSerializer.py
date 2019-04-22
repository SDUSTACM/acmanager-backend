from rest_framework import serializers

from rest_api.models.Training import Training, Stage, Contest, Round


class TrainingListSerializer(serializers.ListSerializer):
    pass
    # def create(self, validated_data):
    #     books = [UserOJAccount(**item) for item in validated_data]
    #     return UserOJAccount.objects.bulk_create(books)


class TrainingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ('id', 'name', 'description', 'create_user', 'create_time')


class TrainingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        training = Training(name=validated_data.get("name"),
                            description=validated_data.get("description"),
                            create_user=validated_data["create_user"])
        training.save()
        return training


class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('name', 'training', 'description')

    def create(self, validated_data):
        stage = Stage(name=validated_data.get("name"),
                            description=validated_data.get("description"),
                            training=validated_data["training"],
                            create_user=validated_data["create_user"]
                      )
        stage.save()
        return stage


# class StageDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stage
#         fields = ('name', 'training', 'description', 'create_user', 'create_time')


class TrainingStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
        # fields= ('id', 'name', 'description', 'training', 'create_user', 'create_time')
        extra_kwargs = {
            'id': {'read_only': True},
            'create_user': {'read_only': True },
            'create_time': {'read_only': True },
            'training': {'read_only': True }
        }

    def create(self, validated_data):
        stage = Stage(name=validated_data.get("name"),
                    description=validated_data.get("description"),
                    training_id=validated_data.get("training_id"),
                    create_user=validated_data["create_user"]
                      )
        stage.save()
        return stage


class TrainingRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        # exclude = ('')
        fields= ('id', 'name', 'description', 'training', 'create_user', 'create_time')
        extra_kwargs = {
            'id': {'read_only': True},
            'create_user': {'read_only': True },
            'create_time': {'read_only': True },
            'training': {'read_only': True }
        }

    def create(self, validated_data):
        _round = Round(name=validated_data.get("name"),
                    description=validated_data.get("description"),
                    training_id=validated_data.get("training_id"),
                    create_user=validated_data["create_user"]
                      )
        _round.save()
        return _round


class StageContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'name', 'description', 'stage','create_user', 'create_time')
        extra_kwargs = {
            'id': {'read_only': True },
            'create_user': {'read_only': True },
            'create_time': {'read_only': True },
            'stage': { 'read_only': True },
        }

    def create(self, validated_data):
        contest = Contest(name=validated_data.get("name"),
                    description=validated_data.get("description"),
                    stage_id=validated_data.get("stage_id"),
                    create_user=validated_data["create_user"]
                      )
        contest.save()
        return contest

#
# class TrainingStageDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stage
#         field = ('name', 'description', 'create_user', 'create_time')