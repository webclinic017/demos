import os
import math
from functools import partial

import yaml
from reflect import (
    ResponsiveValue,
    get_window,
    make_observable,
    CachedEvaluation,
    autorun,
)
from reflect import print_debug
from reflect_html import a, div, img, path, svg, style
from reflect_swiper import Swiper, SwiperSlide
from website.common import BACKGROUND_COLOR, FONT_FAMILY, GREEN, LIGHT_BLUE
from website.home import SLOGAN
from website.main import HTML_LINKS
from website.reflect.gallery import MENU as GALLERY_MENU

TITLE = "Early adopters presentation"
BODY_STYLE = {"backgroundColor": "rgb" + str(BACKGROUND_COLOR), "fontSize": 10}
CSS = ["test.css"]
RIGHT_ARROW = 39
LEFT_ARROW = 37
LOGO_HEIGHT = 52
BOTTOM_HEIGHT = 52
HOME_PAGE = "website.home"
ANSWER_PADDING = 10
# overall height of a title line wrt to the font size
QUESTION_LINE_HEIGHT_RATIO = 70.45 / 48
# overall height of a title line wrt to the font size
ANSWER_LINE_HEIGHT_RATIO = 42 / 36
QUESTION_REM = 2
QUESTION_WIDTH_RATIO = 1234 / 47 / 48  # empirical width of a char wrt its height
ANSWER_WIDTH_RATIO = 1454 / 101 / 36  # empirical width of a char wrt its height
ANSWER_REM = 1.5
MARGIN_TOP_LOGO = 1
maximize = "M396.795 396.8H320V448h128V320h-51.205zM396.8 115.205V192H448V64H320v51.205zM115.205 115.2H192V64H64v128h51.205zM115.2 396.795V320H64v128h128v-51.205z"
minimize = "M64 371.2h76.795V448H192V320H64v51.2zm76.795-230.4H64V192h128V64h-51.205v76.8zM320 448h51.2v-76.8H448V320H320v128zm51.2-307.2V64H320v128h128v-51.2h-76.8z"


def select_file_extension(file_path):
    for extension in ["gif", "png", "svg", "jpg"]:
        maybe_path = f"{file_path}.{extension}"
        if os.path.exists(maybe_path):
            return maybe_path


def title(content, color=LIGHT_BLUE, fontSize="2rem"):
    return div(
        content,
        style={
            "color": color,
            "fontFamily": FONT_FAMILY,
            "fontSize": fontSize,
            "textAlign": "center",
            "margin": fontSize,
        },
    )


def add_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d.items())
    return result


def roman_numeral(number):
    if number <= 3:
        return "I" * number
    if number == 4:
        return "IV"
    if number >= 5:
        return "V" + roman_numeral(number - 5)


def create_icon(
    path_d, style={}, fill="currentColor", width=15, height=15, onClick=None
):
    return svg(
        path(d=path_d),
        viewBox="0 0 512 512",
        width=width,
        height=height,
        fill=fill,
        style=style,
        onClick=onClick,
    )


STYLE = {
    "position": "absolute",
    "bottom": "10px",
}


def left_center_right(left, center, right):
    content = []
    if left:
        content.append(div(left, style={"float": "left"}))
    if right:
        content.append(div(right, style={"float": "right"}))
    if center:
        content.append(div(center, style={"margin": "0 auto", "width": "fit-content"}))
    return div(content, style={"width": "100%"})


def create_bullet(color="white", transparent=True, onClick=None):
    STYLE = {
        "width": "10px",
        "height": "10px",
        "display": "inline-block",
        "border": "1px solid " + color,
        "background": "transparent" if transparent else color,
        "margin": "3.33333px",
        "borderRadius": "50%",
        "pointerEvents": "all",
        "cursor": "pointer",
    }
    return div(None, size=10, style=STYLE, onClick=onClick)


def create_answer_box(answer, details, detail_level):
    update_detail_level = lambda: detail_level.set(1 if detail_level() == 2 else 2)
    return div(
        div(
            [
                div(
                    lambda: answer + ("" if detail_level() == 2 else ".."),
                    onClick=update_detail_level,
                ),
                lambda: div(
                    details,
                    onClick=update_detail_level,
                )
                if detail_level() == 2
                else None,
            ]
        ),
        style={
            # "marginRight": "10px",
            # "marginBottom": "20px",
            "fontSize": f"{ANSWER_REM}rem",
            "color": LIGHT_BLUE,
            "borderColor": GREEN,
            "borderStyle": "dashed",
            "padding": ANSWER_PADDING,
            "display": "inline-block",
            "pointerEvents": "all",
            "cursor": "pointer",
            "textAlign": "justify",
        },
    )


def nb_lines(content, line_length):
    return math.ceil(len(content) / line_length)


def app():
    window = get_window()
    is_touch_screen = window.is_touch_screen
    file_name = window.hash().split("/")[0]
    content = yaml.safe_load(open(f"demos/presentations/{file_name}.yaml", "r").read())
    full_screen = make_observable(False)
    details_level = make_observable(1)
    margin = ResponsiveValue(xs=3, sm=10, md=10, lg=15, xl=None, xxl=30)
    image = Swiper(
        [
            SwiperSlide(
                [
                    img(
                        dataSrc=select_file_extension(
                            os.path.join(
                                os.path.split(app_path.split("#")[0])[0], "default"
                            )
                        ),
                        style={"width": "100%"},
                        className="swiper-lazy",
                        custom_attributes={"data-swipe-ignore": True},
                    ),
                    div(className="swiper-lazy-preloader-white"),
                ]
            )
            for name, app_path in GALLERY_MENU[:-1]  # excluding presentation
        ],
        navigation=True,
        style={"width": "100%"},
    )
    main_page = div(
        [
            title(SLOGAN, LIGHT_BLUE, fontSize="2rem"),
            div(image, custom_attributes={"data-swipe-ignore": True}),
            title(
                "Early adopters presentation",
                color=GREEN,
                fontSize="1.5rem",
            ),
        ],
    )

    def create_question_and_answer(
        default_detail_level_value, on_drill_down, question, answer, details
    ):
        detail_level = make_observable(default_detail_level_value)

        def drill():
            on_drill_down(detail_level)
            detail_level.set(
                default_detail_level_value
                + (0 if detail_level() != default_detail_level_value else 1)
            )

        return div(
            [
                div(
                    question,
                    onClick=drill,
                    style={
                        "fontFamily": FONT_FAMILY,
                        "color": GREEN,
                        "fontSize": f"{QUESTION_REM}rem",
                        "padding": 0,
                        "margin": 0,
                        "pointerEvents": "all",
                        "cursor": "pointer",
                        "textAlign": "center" if is_touch_screen else None,
                    },
                ),
                lambda: create_answer_box(answer, details, detail_level)
                if detail_level() > 0
                else None,
            ]
        )

    def create_page(items, default_detail_level_value):
        current_detail_level = None

        def on_drill_down(new_detail_level):
            nonlocal current_detail_level
            if (
                current_detail_level is not None
                and current_detail_level is not new_detail_level
            ):
                current_detail_level.set(default_detail_level_value)
            current_detail_level = new_detail_level

        return div(
            [
                create_question_and_answer(
                    default_detail_level_value, on_drill_down, *item
                )
                for item in items
            ],
            style={
                # "maxHeight": f"calc(100vh - {BOTTOM_HEIGHT + LOGO_HEIGHT}px)",
                "overflowY": "scroll",
                "paddingTop": 10,
            },
        )

    def generate_slides():
        resolution = window.width() * window.height() / 1000
        font_size = 16
        if resolution > 800:
            font_size = 24
        window.update_tag_style([(f"font-size", f"{font_size}px")], "html")
        details_level_value, width_value, margin_value = (
            details_level(),
            window.width(),
            margin(),
        )
        content_height, max_drill_down_height = 0, 0
        actual_width = width_value * (1.0 - 2 * margin_value / 100)
        nb_chars_title = actual_width / (
            QUESTION_REM * font_size * QUESTION_WIDTH_RATIO
        )
        nb_chars_answer = (actual_width - 2 * ANSWER_PADDING) / (
            QUESTION_REM * font_size * ANSWER_WIDTH_RATIO
        )
        page_height = window.height() - (
            MARGIN_TOP_LOGO * font_size + LOGO_HEIGHT + BOTTOM_HEIGHT
        )
        slides, current_page, current_height = [], [], 0
        question_line_height = QUESTION_LINE_HEIGHT_RATIO * QUESTION_REM * font_size
        answer_line_height = ANSWER_LINE_HEIGHT_RATIO * ANSWER_REM * font_size
        for question, answer, details in content:
            drill_down_height = 0
            content_height = question_line_height * nb_lines(question, nb_chars_title)
            answer_height = answer_line_height * nb_lines(answer, nb_chars_answer)
            details_height = answer_line_height * nb_lines(details, nb_chars_answer)
            if details_level_value >= 1:
                content_height += answer_height
            else:
                drill_down_height += answer_height
            if details_level_value >= 2:
                content_height += details_height
            else:
                drill_down_height += details_height
            max_drill_down_height = max(drill_down_height, max_drill_down_height)
            if current_height + content_height + max_drill_down_height > page_height:
                current_height, max_drill_down_height, current_page, previous_page = (
                    0,
                    0,
                    [],
                    current_page,
                )
                slides.append(create_page(previous_page, details_level()))
            current_page.append((question, answer, details))
            current_height += content_height
        slides.append(create_page(current_page, details_level()))
        return [main_page] + slides

    def page_index():
        args = window.hash().split("/")
        return min(int(args[1]) if len(args) > 1 else 0, len(slides()) - 1)

    def set_page_index(index):
        window.hash.set(f"{file_name}/{index}")

    def safe_increment(increment):
        nonlocal page_index, set_page_index
        page_index_value = page_index()
        if increment:
            if page_index_value + 1 < len(slides()):
                set_page_index(page_index_value + 1)
        else:
            if page_index_value > 0:
                set_page_index(page_index_value - 1)

    window.add_event_listener(
        "fullscreenchange",
        None,
        callback_name=None,
        method=lambda: full_screen.set(not full_screen()),
    )
    window.add_event_listener(
        "swiped",
        "detail.dir",
        lambda d: safe_increment(d == "left") if d in ["left", "right"] else None,
    )
    window.add_event_listener(
        "keydown",
        "keyCode",
        lambda k: k in (RIGHT_ARROW, LEFT_ARROW) and safe_increment(k == RIGHT_ARROW),
    )
    slides = CachedEvaluation(generate_slides)
    full_screen_icon = create_icon(
        lambda: minimize if full_screen() else maximize,
        fill="white",
        width="2.5vh",
        height="2.5vh",
        style={
            "pointerEvents": "all",
            "cursor": "pointer",
        },
        onClick=lambda: window.update_full_screen(not full_screen()),
    )
    detail_level_icon = img(
        src=lambda: f"demos/presentation/menu-icon-{details_level() + 1}.svg",
        style=dict(width="1.6vh", pointerEvents="all", cursor="pointer"),
        onClick=lambda: details_level.set((details_level() + 1) % 3),
    )

    def page_bullets():
        style_ = {
            "width": "10px",
            "height": "10px",
            "size": "10px",
            "position": "relative",
        }
        page_index_value = page_index()
        return (
            # [div(div(None, className="swiper-button-prev"), style=style_)]
            # +
            [
                create_bullet(
                    transparent=page_index_value != index,
                    color="white",
                    onClick=partial(set_page_index, index),
                )
                for index in range(len(slides()))
            ]
            # + [(div(">", style={"color": "white"}))]
        )

    if is_touch_screen:
        icons = left_center_right(detail_level_icon, None, page_bullets)
    else:
        icons = left_center_right(full_screen_icon, detail_level_icon, page_bullets)
    bottom = div(
        icons,
        style={
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "100%",
            "marginLeft": "2rem",
            "marginRight": "2rem",
        },
    )

    def responsive_margins(content, style):
        return div(
            content,
            style=lambda: add_dicts(
                style, {"paddingLeft": f"{margin()}vh", "paddingRight": f"{margin()}vh"}
            ),
        )

    logo_style = {"height": f"calc({LOGO_HEIGHT}px + {MARGIN_TOP_LOGO}rem"}
    if is_touch_screen:
        logo_style.update(marginLeft="auto", marginRight="auto")

    return div(
        [
            div(
                a(
                    img(
                        alt="pytek logo",
                        src="website/static/cogs_pytek.svg",
                        style={
                            "height": LOGO_HEIGHT,
                            "marginLeft": "2rem",
                            "marginTop": f"{MARGIN_TOP_LOGO}rem",
                        },
                    ),
                    href="https://pytek.io",
                    target="_blank",
                ),
                style=logo_style,
            ),
            responsive_margins(
                div(
                    lambda: slides()[page_index()],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "height": "100%",
                    },
                ),
                style={
                    "flex": 1,
                    "overflowY": "scroll",
                    "maxHeight": f"calc(100vh - {LOGO_HEIGHT + BOTTOM_HEIGHT}px)",
                },
            ),
            # dummy bottom div to ensure the main one is centered
            div(None, style={"height": BOTTOM_HEIGHT}),
            style("swiper-navigation-size: 10px;"),
            div(
                bottom,
                style={
                    "height": BOTTOM_HEIGHT,
                    "width": "100%",
                    "position": "absolute",
                    "bottom": 0,
                },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "height": "100%",
            "justifyContent": "center",
        },
    )