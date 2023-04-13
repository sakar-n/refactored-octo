from django.urls import path
from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    DeleteView,
    CustomLoginView,
    RegisterPage
)
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", TaskList.as_view(), name="task"),
    path("task/<int:pk>/", login_required(TaskDetail.as_view()), name="task"),
    path("task-create/",  login_required(TaskCreate.as_view()), name="task-create"),
    path("task-update/<int:pk>/", login_required(TaskUpdate.as_view()), name="task-update"),
    path("task-delete/<int:pk>/",  login_required(DeleteView.as_view()), name="task-delete"),
    path("register/", RegisterPage.as_view(), name= "register"),
]
