import reflex as rx
from components.navbar import navbar
from components.product_card import product_card
from state.products_state import ProductsState

@rx.page(route="/products", title="Catalog - AI Store", on_load=ProductsState.fetch_products)
def products() -> rx.Component:
    """The generic catalog page showing all products."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading("All Products", size="8"),
                    rx.spacer(),
                    rx.select(
                        ["default", "low_to_high", "high_to_low"],
                        placeholder="Sort by price",
                        on_change=ProductsState.update_sort,
                        width="200px"
                    ),
                    width="100%",
                    margin_top="3rem",
                    margin_bottom="1rem",
                    align_items="center"
                ),
                
                rx.cond(
                    ProductsState.search_query != "",
                    rx.text(f"Showing results for '{ProductsState.search_query}'", color="gray", margin_bottom="1rem"),
                ),
                
                rx.cond(
                    ProductsState.all_products.length() > 0,
                    rx.grid(
                        rx.foreach(ProductsState.all_products, lambda p: product_card(p)),
                        columns="4",
                        spacing="5",
                        width="100%"
                    ),
                    rx.spinner(size="3")
                ),
                
                padding_bottom="5rem",
                width="100%"
            ),
            size="4"
        )
    )
