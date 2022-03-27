from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register('user_api', views.UserApi_modelViewset, basename="user")
router.register('attendence_api',
                views.AttendenceApi_modelViewset, basename="attendence")
router.register('class_api', views.ClassApi_modelViewset, basename="class")
router.register('scheduleclasses_api', views.ScheduleClassesApi_modelViewset,
                basename="scheduleclasses")

urlpatterns = [
    path('decline/<int:pk>/', views.attendence_decline, name="decline"),
    path('approve/<int:pk>/', views.attendence_approve, name="approve"),
    path('timetable/<int:class_id>/', views.show_timetable, name="timetable"),
     path('', include(router.urls)),

    # for JWT
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('verify_token/', TokenVerifyView.as_view(), name='token_verify _view'),
]