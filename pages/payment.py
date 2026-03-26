import reflex as rx
from components.navbar import navbar
from state.cart_state import CartState
from state.user_state import UserState
from state.payment_state import PaymentState

@rx.page(route="/payment", title="Razorpay Checkout")
def payment() -> rx.Component:
    """Professional Razorpay Payment Page with order summary and gateway integration."""
    return rx.box(
        # Load Razorpay's checkout.js
        rx.script(src="https://checkout.razorpay.com/v1/checkout.js"),
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Order Summary", size="8", margin_top="2rem", margin_bottom="1rem"),
                rx.grid(
                    # Left Column: Payment Methods & Details
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(tag="qr_code", size=24, color="blue"),
                                    rx.heading("Scan & Pay with Any UPI App", size="4"),
                                    spacing="2",
                                ),
                                rx.divider(),
                                rx.text("You can also pay directly using the link below:", size="2", color="gray"),
                                rx.link(
                                    rx.button(
                                        "Open Personal Razorpay Link",
                                        color_scheme="green",
                                        variant="outline",
                                        width="100%",
                                    ),
                                    href=CartState.direct_payment_url,
                                    is_external=True,
                                    width="100%",
                                ),
                                rx.text("Pay to: SANJAY KRISHNAN KARTHIKEYAN", size="1", color="gray", margin_top="0.5rem"),
                                width="100%",
                                align_items="start",
                                spacing="4",
                            ),
                            padding="1.5rem",
                            width="100%",
                            shadow="md",
                            margin_top="1rem",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(tag="shield-check", size=24, color="blue"),
                                    rx.heading("Secure Checkout", size="4"),
                                    spacing="2",
                                ),
                                rx.divider(),
                                rx.text("Payment will be processed via Razorpay Secure Gateway.", size="2", color="gray"),
                                rx.badge("Test Mode Active", color_scheme="orange"),
                                width="100%",
                                align_items="start",
                                spacing="4",
                            ),
                            padding="1.5rem",
                            width="100%",
                            shadow="md",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.heading("Shipping Information", size="4"),
                                rx.divider(),
                                rx.text(UserState.customer_display_name, weight="bold"),
                                rx.text("Standard Delivery (3-5 business days)", size="2"),
                                width="100%",
                                align_items="start",
                                spacing="4",
                            ),
                            padding="1.5rem",
                            width="100%",
                            shadow="md",
                            margin_top="1rem",
                        ),
                        width="100%",
                    ),
                    # Right Column: Order Price Breakdown
                    rx.card(
                        rx.vstack(
                            rx.heading("Price Summary", size="4", margin_bottom="1rem"),
                            rx.hstack(
                                rx.text("Subtotal", color="gray"),
                                rx.spacer(),
                                rx.text("₹", CartState.total_price),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Tax (GST 18%)", color="gray"),
                                rx.spacer(),
                                rx.text("₹", CartState.tax_amount),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Delivery Charges", color="gray"),
                                rx.spacer(),
                                rx.text("FREE", color="green"),
                                width="100%",
                            ),
                            rx.divider(margin_y="1rem"),
                            rx.hstack(
                                rx.text("Total Payable", size="5", weight="bold"),
                                rx.spacer(),
                                rx.text(
                                    "₹",
                                    CartState.total_payable,
                                    size="5",
                                    weight="bold",
                                    color="blue",
                                ),
                                width="100%",
                            ),
                            rx.button(
                                "Proceed to Pay with Razorpay",
                                color_scheme="blue",
                                size="4",
                                width="100%",
                                margin_top="2rem",
                                on_click=PaymentState.start_payment,
                                loading=PaymentState.status == "processing",
                            ),
                            rx.cond(
                                PaymentState.status == "failed",
                                rx.callout(
                                    PaymentState.error_message,
                                    icon="alert-circle",
                                    color_scheme="red",
                                    margin_top="1rem",
                                ),
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        padding="2rem",
                        width="100%",
                        shadow="lg",
                        background_color="#fff",
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                    margin_top="1rem",
                ),
                width="100%",
                align_items="center",
            ),
            size="3",
        ),
        background_color="#f2f5f7",
        min_height="100vh",
    )
