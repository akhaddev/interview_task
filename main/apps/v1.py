from django.urls import include, path


urlpatterns = [
    path(
        "user/",
        include(
            ("main.apps.user.urls", "main.apps.user.urls"),
            namespace="user",
        ),
    ),
    path(
        "menu/",
        include(
            ("main.apps.menu.urls", "main.apps.menu.urls"),
            namespace="menu",
        ),
    ),
    path(
        "order/",
        include(
            ("main.apps.order.urls", "main.apps.order.urls"),
            namespace="order",
        ),
    ),
    path(
        "cart/",
        include(
            ("main.apps.cart.urls", "main.apps.cart.urls"),
            namespace="cart",
        ),
    )
]

