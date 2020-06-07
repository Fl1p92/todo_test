from rest_framework.routers import SimpleRouter

from .views import TaskViewSet


router = SimpleRouter()
router.register('', TaskViewSet, basename='todo')
urlpatterns = router.get_urls()
