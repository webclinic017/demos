from reflect_html import *
from reflect_antd import Layout, Menu
from reflect_ant_icons import (
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    BarChartOutlined,
    CloudOutlined,
    AppstoreOutlined,
    TeamOutlined,
    ShopOutlined,
)

Header, Content, Footer, Sider = (
    Layout.Header,
    Layout.Content,
    Layout.Footer,
    Layout.Sider,
)


def app():
    return Layout(
        [
            Sider(
                [
                    div(className="logo"),
                    Menu(
                        [
                            Menu.Item("nav 1", key="1", icon=UserOutlined([])),
                            Menu.Item("nav 2", key="2", icon=VideoCameraOutlined([])),
                            Menu.Item("nav 3", key="3", icon=UploadOutlined([])),
                            Menu.Item("nav 4", key="4", icon=BarChartOutlined([])),
                            Menu.Item("nav 5", key="5", icon=CloudOutlined([])),
                            Menu.Item("nav 6", key="6", icon=AppstoreOutlined([])),
                            Menu.Item("nav 7", key="7", icon=TeamOutlined([])),
                            Menu.Item("nav 8", key="8", icon=ShopOutlined([])),
                        ],
                        theme="dark",
                        mode="inline",
                        defaultSelectedKeys=["4"],
                    ),
                ],
                style=dict(overflow="auto", height="100vh", position="fixed", left=0),
            ),
            Layout(
                [
                    Header(className="site-layout-background", style=dict(padding=0)),
                    Content(
                        div(
                            [
                                "...",
                                br(),
                                "Really",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "long",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "...",
                                br(),
                                "content",
                            ],
                            className="site-layout-background",
                            style=dict(padding=24, textAlign="center"),
                        ),
                        style=dict(margin="24px 16px 0", overflow="initial"),
                    ),
                    Footer(
                        "Ant Design ©2018 Created by Ant UED",
                        style=dict(textAlign="center"),
                    ),
                ],
                className="site-layout",
                style=dict(marginLeft=200),
            ),
        ]
    )
