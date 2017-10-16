from apache.airavata.model.experiment.ttypes import ExperimentModel
from apache.airavata.model.workspace.ttypes import Project
from apache.airavata.model.appcatalog.appdeployment.ttypes import ApplicationModule
from django.conf import settings

from rest_framework import serializers

from urllib.parse import quote


class FullyEncodedHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        lookup_value = getattr(obj, self.lookup_field)
        encoded_lookup_value = quote(lookup_value, safe="")
        # Bit of a hack. Django's URL reversing does URL encoding but it doesn't
        # encode all characters including some like '/' that are used in URL
        # mappings.
        kwargs = {self.lookup_url_kwarg: "__PLACEHOLDER__"}
        url = self.reverse(view_name, kwargs=kwargs, request=request, format=format)
        return url.replace("__PLACEHOLDER__", encoded_lookup_value)

class GetGatewayUsername(object):

    def __call__(self):
        return self.field.context['request'].user.username

    def set_context(self, field):
        self.field = field

class GatewayUsernameDefaultField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = True
        self.default = GetGatewayUsername()

class GatewayIdDefaultField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = True
        self.default = settings.GATEWAY_ID

class ProjectSerializer(serializers.Serializer):
    url = FullyEncodedHyperlinkedIdentityField(view_name='project-detail', lookup_field='projectID', lookup_url_kwarg='pk')
    projectID = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    owner = GatewayUsernameDefaultField()
    gatewayId = GatewayIdDefaultField()
    experiments = FullyEncodedHyperlinkedIdentityField(view_name='api_project_experiments_list', lookup_field='projectID', lookup_url_kwarg='project_id')

    def create(self, validated_data):
        return Project(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        return instance

    def get_username(self):
        return self.context.request.user.username

class ExperimentSerializer(serializers.Serializer):

    experimentId = serializers.CharField(read_only=True)
    projectId = serializers.CharField(required=True)
    project = FullyEncodedHyperlinkedIdentityField(view_name='project-detail', lookup_field='projectId', lookup_url_kwarg='project_id')
    gatewayId = GatewayIdDefaultField()
    experimentType = serializers.CharField(required=True)
    userName = GatewayUsernameDefaultField()
    experimentName = serializers.CharField(required=True)

    def create(self, validated_data):
        return ExperimentModel(**validated_data)

    def update(self, instance, validated_data):
        raise Exception("Not implemented")


class ApplicationModuleSerializer(serializers.Serializer):
    appModuleId=serializers.CharField(required=True)
    appModuleName=serializers.CharField(required=True)
    appModuleDescription = serializers.CharField()
    appModuleVersion=serializers.CharField()

    def create(self, validated_data):
        return ApplicationModule(**validated_data)

    def update(self, instance, validated_data):
        raise Exception("Not implemented")