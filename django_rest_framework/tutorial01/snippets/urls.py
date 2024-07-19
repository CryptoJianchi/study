from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

from rest_framework import renderers
from snippets.views import api_root, SnippetViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("snippets/", views.snippet_list),
    path("snippets/<int:pk>/", views.snippet_detail),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path("", views.api_root),
    path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view()),
]

# 登录和注销
urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# 教程05 API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root),
        path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
        path(
            "snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"
        ),
        path(
            "snippets/<int:pk>/highlight/",
            views.SnippetHighlight.as_view(),
            name="snippet-highlight",
        ),
        path("users/", views.UserList.as_view(), name="user-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    ]
)


# 教程06 视图集和路由器

# 方式一：将 ViewSet 明确绑定到 URL
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

# 方式二：使用路由器， 自动按约定形成路由
# 向路由器注册对应的视图集，它将完成剩下的工作
# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

#视图与视图集之间的权衡
#使用 ViewSet 是一种非常有用的抽象。它确保URL与API中的约定一致，最大限度地减少代码量，专注于 API 提供的交互和表示，而不是 URL 配置的细节。
#这并不意味着它总是正确的方法。在使用基于类的视图而不是基于函数的视图时，需要考虑一系列类似的权衡。使用 ViewSet 不如单独构建 API 视图那么明确。