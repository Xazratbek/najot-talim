from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookViewSet

# from django.urls import path
# from .views import BookModelViewSet
# from rest_framework import routers
# from django.urls import include

# router = routers.SimpleRouter()
# router.register(r'book', BookModelViewSet)

# urlpatterns = [
#     # path('', BookGenericAPIView.as_view()),
#     # path('<int:pk>/', BookGenericAPIView.as_view()),
#     # path('create/', BookGenericAPIView.as_view()),
#     # path('update/<int:pk>/', BookGenericAPIView.as_view()),
#     # path('delete/<int:pk>/', BookGenericAPIView.as_view()),
#     # path('', BookModelViewSet.as_view({'get': 'list', 'post': 'create'})),
#     # path('<int:pk>/', BookModelViewSet.as_view({
#     #     'get': 'retrieve',
#     #     'put': 'update',
#     #     'patch': 'partial_update',
#     #     'delete': 'destroy'
#     # })),
#     path('api/v1/', include(router.urls))
# ]


router = SimpleRouter()
router.register(r'book', BookViewSet)

urlpatterns = router.urls
