import reflex as rx
from state.user_state import UserState
from state.recommendation_state import RecommendationState
from components.navbar import navbar
from components.product_card import product_card

@rx.page(route="/", title="Home - AI Store", on_load=RecommendationState.fetch_general_recommendations)
def home() -> rx.Component:
    """The landing page. Shows different headings based on user type."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Welcome to Your AI-Powered Store!", size="9", margin_top="3rem", margin_bottom="1rem", text_align="center"),
                rx.text("Discover products perfectly tailored for you using Machine Learning.", size="4", color="gray", margin_bottom="3rem", text_align="center"),
                
                # Dynamic heading based on UserState User Flow concept
                rx.cond(
                    UserState.is_new_user,
                    # If new user or not logged in -> rating based heading
                    rx.heading("Top Rated Products Just For You", size="6", margin_bottom="1rem"),
                    # If existing logged in user -> Collaborative heading as per prompt
                    rx.heading("Similar user's like your also liked", size="6", margin_bottom="1rem") 
                ),
                
                rx.button(
                    "Load My Recommendations", 
                    on_click=RecommendationState.fetch_general_recommendations, 
                    size="3", 
                    color_scheme="indigo", 
                    margin_bottom="2rem"
                ),
                
                rx.cond(
                    RecommendationState.is_loading,
                    rx.spinner(size="3"),
                    rx.grid(
                        rx.foreach(RecommendationState.recommendations, lambda p: product_card(p)),
                        columns="4",
                        spacing="4",
                        width="100%"
                    )
                ),
                
                padding_bottom="4rem",
                width="100%",
                align_items="center"
            ),
            size="4"
        )
    )
