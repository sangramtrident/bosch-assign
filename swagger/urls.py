from django.conf.urls import url

from swagger.swagger_views import schema_view

urlpatterns = [
    # Swagger docs api
    url(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
