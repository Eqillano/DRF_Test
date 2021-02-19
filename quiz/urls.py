from django.conf.urls import include, url

from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import QuizViewSet, QuestionViewSet, SummaryViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'quiz', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'summary', SummaryViewSet)

urlpatterns = [
    url(r'api/', include((router.urls))),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
]
