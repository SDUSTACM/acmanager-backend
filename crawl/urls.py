from django.urls import path

from crawl.views import VjudgeSolveListView, UVASolveListView, SolveCountView, SolveCountListView, UserOJAccountView

urlpatterns = [
    path('solve_list/vjudge/<username>/', VjudgeSolveListView.as_view(), name="solve-list-vjudge-view"),
    path('solve_list/uva/<username>/', UVASolveListView.as_view(), name="solve-list-uva-view"),
    path('solve_count/<username>/', SolveCountView.as_view(), name="solve-count-detail-view"),
    path('solve_count/', SolveCountListView.as_view(), name="solve_count-view"),
    path('oj_account/<username>/', UserOJAccountView.as_view(), name="solve_count-view")
    # path('api/', include('rest_api.urls')),
]