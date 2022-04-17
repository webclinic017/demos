"""Allows to quickly navigate between apps displaying code and preview."""

import os

from reflect import get_window, Component
from reflect_html import a, div, img
from reflect_monaco import Editor as CodeEditor
from reflect_rcdock import DockLayoutReflect
from reflect_utils import create_file_explorer, evaluate_demo_module, get_module_name

TITLE = "App explorer"
ALMOST_BLACK = "#0f1724"


def app():
    base_path = get_window().hash()
    counter = 0

    def create_tab(title, application):
        nonlocal counter
        counter += 1
        return {
            "id": str(counter),
            "title": div(title) if callable(title) else title,
            "content": application,
            "cached": True,
        }

    current_path, tree = create_file_explorer(
        base_path, folder_filter=lambda p: p.startswith("__")
    )

    def actual_path():
        if current_path():
            result = os.path.join(base_path, current_path())
            return None if os.path.isdir(result) else result

    relative_path = lambda: actual_path() or "No app selected"

    def component():
        actual_path_value = actual_path()
        if actual_path_value:
            extension = actual_path_value.rsplit(".", 1)[-1]
            if extension == "py":
                _success, _css, _title, component = evaluate_demo_module(
                    get_module_name(actual_path()), {}
                )
                return (
                    component if isinstance(component, Component) else component.content
                )
            elif extension in ["svg"]:
                return img(src=actual_path_value)
            else:
                return div(None)

    editor = div(
        lambda: CodeEditor(
            defaultValue=open(actual_path(), "r").read(),
            options=dict(
                minimap={"enabled": False},
                lineNumbers=True,
                glyphMargin=False,
                wordWrap=True,
                readOnly=True,
            ),
            defaultLanguage="python",
            height=600,
        )
        if actual_path()
        else None
    )
    defaultLayout = {
        "dockbox": {
            "mode": "horizontal",
            "children": [
                {
                    "size": 1,
                    "tabs": [("Apps", tree)],
                },
                {
                    "size": 3,
                    "mode": "vertical",
                    "children": [
                        {
                            "size": 2,
                            "tabs": [
                                (
                                    relative_path,
                                    editor,
                                ),
                            ],
                        },
                        {
                            "size": 1,
                            "tabs": [
                                (
                                    "Preview",
                                    div(
                                        component,
                                        style={
                                            "height": "inherit",
                                            "width": "inherit",
                                            "padding": 20,
                                        },
                                    ),
                                )
                            ],
                        },
                    ],
                },
            ],
        }
    }
    return div(
        [
            div(
                [
                    div(
                        "App explorer",
                        style={
                            "padding": ".5rem",
                            "fontSize": "1.5rem",
                            "color": "white",
                            "marginLeft": "2rem",
                        },
                    ),
                    div(
                        lambda: a(
                            "launch",
                            href=lambda: "/app/" + actual_path()[:-3],
                            target="_blank",
                            title=lambda: f"Launch {actual_path()}",
                        )
                        if actual_path()
                        else None,
                        style={
                            "padding": ".5rem",
                            "fontSize": "1.0rem",
                            "color": "white",
                            "marginLeft": "auto",
                            "marginRight": "2rem",
                        },
                    ),
                ],
                style={
                    "backgroundColor": ALMOST_BLACK,
                    "display": "flex",
                    "alignItems": "center",
                },
            ),
            DockLayoutReflect(
                defaultLayout=defaultLayout,
                style={"flex": 2},
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "minHeight": "100%",
        },
    )